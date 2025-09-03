from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:event_id>/", views.add_to_cart, name="add_to_cart"),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("checkout/", views.checkout, name="checkout"),
    path("clear/", views.clear_cart, name="clear_cart"),
    path("remove-coupon/", views.remove_coupon, name="remove_coupon"),
]
