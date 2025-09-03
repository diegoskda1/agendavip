from django.contrib import admin
from .models import Coupon, CartItem, Order

# ===============================
# Admin do Cupom
# ===============================
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code", "discount_percent", "active", "usage_count", "usage_limit",
        "valid_from", "valid_until", "created_at"
    )
    list_filter = ("active", "valid_from", "valid_until")
    search_fields = ("code",)
    readonly_fields = ("created_at", "updated_at", "usage_count")
    ordering = ("-created_at",)


# ===============================
# Admin de Itens do Carrinho
# ===============================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("event", "seat_type", "quantity", "price_per_ticket", "session_key")
    list_filter = ("seat_type", "event")
    search_fields = ("event__name", "seat_type", "session_key")


# ===============================
# Admin de Pedidos
# ===============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "event", "subtotal", "admin_fee", "discount_amount", "final_price", "created_at")
    readonly_fields = ("id", "final_price", "created_at", "updated_at")  # apenas campos que não devem ser alterados manualmente
    list_filter = ("event", "customer")
    search_fields = ("customer__username", "event__name")
