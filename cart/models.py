from django.db import models
from django.utils import timezone
from accounts.models import User
from events.models import Event, EventSeats
from decimal import Decimal

# =========================
# Cupom de desconto
# =========================
class Coupon(models.Model):
    code = models.CharField("Código do Cupom", max_length=50, unique=True)
    discount_percent = models.DecimalField(
        "Percentual de Desconto (%)",
        max_digits=5,
        decimal_places=2
    )
    active = models.BooleanField("Ativo", default=True)
    valid_from = models.DateTimeField("Válido a partir de", default=timezone.now)
    valid_until = models.DateTimeField("Válido até", null=True, blank=True)
    usage_limit = models.PositiveIntegerField(
        "Quantidade de usos",
        null=True, blank=True
    )
    usage_count = models.PositiveIntegerField("Usos realizados", default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    def is_valid(self):
        now = timezone.now()
        within_limit = True
        if self.usage_limit is not None:
            within_limit = self.usage_count < self.usage_limit
        return self.active and self.valid_from <= now and (self.valid_until is None or self.valid_until >= now) and within_limit

    def use(self):
        if self.usage_limit is None or self.usage_count < self.usage_limit:
            self.usage_count += 1
            self.save()


# =========================
# Itens do carrinho
# =========================
class CartItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal("0.00"))
    session_key = models.CharField(max_length=40, db_index=True, default="unknown")

    # Campos automáticos do evento
    event_name = models.CharField(max_length=200, blank=True)
    event_start_time = models.DateTimeField(null=True, blank=True)
    event_venue = models.CharField(max_length=200, blank=True)
    event_cover_image = models.ImageField(upload_to='cart_event_covers/', null=True, blank=True)

    @property
    def subtotal(self):
        return self.quantity * (self.price_per_ticket or Decimal("0.00"))

    def save(self, *args, **kwargs):
        if self.event:
            self.event_name = self.event.name
            self.event_start_time = self.event.start_time
            self.event_venue = self.event.venue.name if self.event.venue else ""
            self.event_cover_image = self.event.cover_image

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.seat_type} - {self.event_name}"


# =========================
# Pedido
# =========================
# cart/models.py
from django.db import models
from decimal import Decimal
from accounts.models import User
from events.models import Event

class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    subtotal = models.DecimalField(
        "Subtotal", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    # Taxa de serviço agora é totalmente manual
    admin_fee = models.DecimalField(
        "Taxa de Serviço", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    discount_amount = models.DecimalField(
        "Desconto", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Garante que não existam dois pedidos para o mesmo usuário e evento
        unique_together = ('customer', 'event')
        ordering = ['-created_at']

    @property
    def final_price(self):
        """
        Retorna o valor final do pedido somando subtotal + taxa e subtraindo desconto.
        """
        return (self.subtotal or Decimal("0.00")) + (self.admin_fee or Decimal("0.00")) - (self.discount_amount or Decimal("0.00"))

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer} ({self.event})"

