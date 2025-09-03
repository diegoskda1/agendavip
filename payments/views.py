import json
import hmac
import hashlib
import mercadopago
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from cart.models import Order
from .models import Payment

# Inicializa SDK com o token correto
sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
WEBHOOK_SECRET = settings.MERCADOPAGO_WEBHOOK_SECRET
BASE_URL = settings.DEVELOPMENT_URL if settings.DEBUG else settings.PRODUCTION_URL


@login_required
def mercadopago_checkout(request, order_id, payment_type="checkout"):
    order = get_object_or_404(Order, id=order_id)

    if not order.cart_items.exists():
        messages.error(request, "Seu pedido não possui itens válidos.")
        return redirect("cart:cart_detail")

    payer_info = {
        "name": request.user.get_full_name() or request.user.username,
        "email": request.user.email or f"user_{request.user.id}@example.com",
    }

    try:
        if payment_type.lower() == "pix":
            payment_data = {
                "transaction_amount": float(order.final_price or 0),
                "description": f"Pedido #{order.id}",
                "payment_method_id": "pix",
                "payer": payer_info,
                "external_reference": str(order.id),
            }
            payment_response = sdk.payment().create(payment_data)
            payment_info = payment_response.get("response", {})

            qr_code = payment_info.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code")
            qr_code_base64 = payment_info.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")

            if not payment_info.get("id"):
                return render(request, "payments/checkout_error.html", {"order": order, "error": "Não foi possível criar o pagamento Pix."})

            Payment.objects.create(
                user=request.user,
                event=order.cart_items.first().event if order.cart_items.exists() else None,
                amount=order.final_price,
                payment_id=str(payment_info.get("id")),
                status=payment_info.get("status", "pending"),
            )

            return render(request, "payments/checkout.html", {
                "qr_code": qr_code,
                "qr_code_base64": qr_code_base64,
                "order": order,
                "amount": order.final_price
            })

        # Checkout padrão (Cartão, etc.)
        preference_data = {
            "items": [{
                "title": f"Pedido #{order.id}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(order.final_price or 0)
            }],
            "payer": payer_info,
            "back_urls": {
                "success": f"{BASE_URL}/payments/success/?external_reference={order.id}",
                "failure": f"{BASE_URL}/payments/failure/?external_reference={order.id}",
                "pending": f"{BASE_URL}/payments/pending/?external_reference={order.id}"
            },
            "notification_url": f"{BASE_URL}/payments/webhook/",
            "auto_return": "approved",
            "external_reference": str(order.id),
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        if "init_point" in preference:
            Payment.objects.create(
                user=request.user,
                event=order.cart_items.first().event if order.cart_items.exists() else None,
                amount=order.final_price,
                payment_id=str(preference.get("id")),
                status="pending",
            )
            return redirect(preference["init_point"])

        error_message = preference.get("message") or preference.get("error") or "Erro ao criar preferência de pagamento."
        return render(request, "payments/checkout_error.html", {"order": order, "error": error_message})

    except Exception as e:
        print("Erro no checkout:", str(e))
        return render(request, "payments/checkout_error.html", {"order": order, "error": f"Erro ao conectar com Mercado Pago: {str(e)}"})


def success(request):
    order_id = request.GET.get("external_reference")
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/success.html', {"order": order})


def failure(request):
    order_id = request.GET.get("external_reference")
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/failure.html', {'order': order})


def pending(request):
    order_id = request.GET.get("external_reference")
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/pending.html', {'order': order})


@login_required
def cancel(request, order_id=None):
    return render(request, 'payments/cancel.html')


@csrf_exempt
def payment_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "method_not_allowed"}, status=405)

    try:
        payload = request.body
        received_signature = request.headers.get("X-Hub-Signature")

        # Valida assinatura apenas se o header existir
        if received_signature:
            computed_signature = hmac.new(WEBHOOK_SECRET.encode("utf-8"), payload, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(received_signature, computed_signature):
                return JsonResponse({"error": "Assinatura inválida"}, status=400)

        data = json.loads(payload.decode("utf-8"))

        # Aceita eventos de pagamento
        if data.get("type") not in ["payment", "payment.updated"]:
            return JsonResponse({"status": "ignored"}, status=200)

        payment_id = data.get("data", {}).get("id")

        # ⚠️ Se for teste (ID não existe), evita erro
        if not payment_id or payment_id == "123456":
            # Log de teste
            print("Webhook de teste recebido:", data)
            return JsonResponse({"status": "ok", "message": "Teste recebido"}, status=200)

        # Busca pagamento real no SDK
        payment_info = sdk.payment().get(payment_id).get("response", {})

        status = payment_info.get("status")
        amount = payment_info.get("transaction_amount")
        external_reference = payment_info.get("external_reference")

        # Atualiza ou cria pagamento no DB
        payment = Payment.objects.filter(payment_id=str(payment_id)).first()
        if not payment:
            order = Order.objects.filter(id=external_reference).first() if external_reference else None
            payment = Payment.objects.create(
                user=order.customer if order else None,
                event=order.cart_items.first().event if order and order.cart_items.exists() else None,
                amount=amount,
                payment_id=str(payment_id),
                status=status,
            )
        else:
            payment.status = status
            payment.save()

        return JsonResponse({"status": "ok"}, status=200)

    except Exception as e:
        print("Erro no webhook:", str(e))
        return JsonResponse({"error": str(e)}, status=400)
