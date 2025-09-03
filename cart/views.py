# cart/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from events.models import Event, EventSeats
from .models import CartItem, Order, Coupon
# cart/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from events.models import Event, EventSeats
from .models import CartItem, Order, Coupon

@login_required
def add_to_cart(request, event_id):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    event = get_object_or_404(Event, id=event_id)

    # Limpa cupom aplicado sempre que o carrinho muda
    request.session.pop("coupon_id", None)

    try:
        seats = event.event_seats
    except EventSeats.DoesNotExist:
        messages.error(request, "Este evento não possui assentos cadastrados.")
        return redirect("events:event_detail", pk=event_id)

    vip_qty = int(request.POST.get("vip_quantity", 0))
    normal_qty = int(request.POST.get("normal_quantity", 0))
    openbar_qty = int(request.POST.get("openbar_quantity", 0))

    # Função auxiliar para criar ou atualizar item
    def add_item(seat_type, quantity, price):
        if quantity > 0 and price is not None:
            item, created = CartItem.objects.get_or_create(
                event=event,
                seat_type=seat_type,
                session_key=session_key,
                order=None,  # não associar a pedido ainda
                defaults={"price_per_ticket": price, "quantity": 0},
            )
            item.quantity += quantity
            item.save()

    add_item("vip", vip_qty, seats.price_vip)
    add_item("normal", normal_qty, seats.price)
    add_item("openbar", openbar_qty, seats.price_openbar)

    messages.success(request, "Ingressos adicionados ao carrinho com sucesso!")
    return redirect("cart:cart_detail")

@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code", "").strip()
        if not code:
            messages.error(request, "Digite um código de cupom.")
            return redirect("cart:cart_detail")

        try:
            coupon = Coupon.objects.get(code__iexact=code)
            if coupon.is_valid():
                request.session["coupon_id"] = coupon.id
                messages.success(request, f"Cupom {code} aplicado com sucesso!")
                return redirect("/cart/?applied=1")
            else:
                messages.error(request, "Este cupom não é válido ou está expirado.")
        except Coupon.DoesNotExist:
            messages.error(request, "Cupom inválido.")
    return redirect("cart:cart_detail")


@login_required
def remove_coupon(request):
    """
    Endpoint para remover manualmente o cupom.
    """
    request.session.pop("coupon_id", None)
    messages.info(request, "Cupom removido.")
    return redirect("cart:cart_detail")


@login_required
def checkout(request):
    """
    (Se você não usa esse checkout, pode remover.)
    Mantido aqui só como exemplo isolado; seu fluxo usa cart_detail -> pagarme_checkout.
    """
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    discount = 0
    coupon_code = request.POST.get('coupon', '').strip()

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            discount = (total * coupon.discount_percent) / 100
        except Coupon.DoesNotExist:
            messages.error(request, "Cupom inválido ou expirado.")

    final_total = total - discount

    return render(request, 'checkout.html', {
        'cart': cart,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    })


@login_required
def clear_cart(request):
    CartItem.objects.filter(session_key=request.session.session_key).delete()
    request.session.pop("coupon_id", None)
    messages.info(request, "Carrinho limpo com sucesso!")
    return redirect("cart:cart_detail")


from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, Coupon

@login_required
def cart_detail(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.GET.get("applied") != "1":
        request.session.pop("coupon_id", None)

    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        context = {
            "cart_items": [],
            "orders": [],
            "total_price": Decimal("0.00"),
            "discount_amount": Decimal("0.00"),
            "final_price": Decimal("0.00"),
        }
        return render(request, "cart/cart_detail.html", context)

    discount_amount = Decimal("0.00")
    coupon_id = request.session.get("coupon_id")
    total_items_price = sum(item.subtotal for item in cart_items)

    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid():
                discount_amount = (coupon.discount_percent / Decimal("100")) * total_items_price
            else:
                request.session.pop("coupon_id", None)
        except Coupon.DoesNotExist:
            request.session.pop("coupon_id", None)

    orders = {}
    for item in cart_items:
        event = item.event
        if event.id not in orders:
            order, created = Order.objects.get_or_create(
                customer=request.user,
                event=event,
                defaults={
                    "subtotal": Decimal("0.00"),
                    "discount_amount": Decimal("0.00"),
                    "admin_fee": Decimal("0.00"),
                },
            )
            orders[event.id] = order
        else:
            order = orders[event.id]

        order_items = (CartItem.objects.filter(event=event, session_key=session_key) | CartItem.objects.filter(event=event, order=order)).distinct()
        order.subtotal = sum(ci.subtotal for ci in order_items)
        order.discount_amount = discount_amount
        order.save()

        for ci in order_items:
            if ci.order != order:
                ci.order = order
                ci.save()

    main_order = next(iter(orders.values()))

    cart_items = CartItem.objects.filter(session_key=session_key)

    final_price = main_order.subtotal + main_order.admin_fee - discount_amount

    context = {
        "cart_items": cart_items,
        "orders": orders.values(),
        "order": main_order,
        "total_price": total_items_price,
        "discount_amount": discount_amount,
        "final_price": final_price,
    }

    return render(request, "cart/cart_detail.html", context)
