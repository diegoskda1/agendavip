from django.db import models
from django.conf import settings
from events.models import Event
from cart.models import Order
import uuid

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID do Ticket")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets", verbose_name="Usuário")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Evento")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Pedido")
    seat_type = models.CharField(max_length=50, verbose_name="Tipo de Assento")  # vip, normal, etc.
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Data da Compra")
    qr_code_image = models.ImageField(upload_to="tickets_qr/", blank=True, null=True, verbose_name="QR Code do Ticket")

    def __str__(self):
        return f"{self.event.name} - {self.user.username} ({self.seat_type})"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-purchase_date"]
