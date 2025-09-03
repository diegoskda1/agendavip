from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("cart_checkout/<int:order_id>/", views.mercadopago_checkout, name="mercadopago_checkout"),
    path("success/<int:order_id>/", views.success, name="payment_success"),
    path("failure/<int:order_id>/", views.failure, name="payment_failure"),
    path("pending/<int:order_id>/", views.pending, name="payment_pending"),
    path("cancel/<int:order_id>/", views.cancel, name="payment_cancel"),
    path("webhook/", views.payment_webhook, name="payment_webhook"),
]
