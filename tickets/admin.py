from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "seat_type", "purchase_date")
    list_filter = ("event", "seat_type", "purchase_date")
    search_fields = ("user__username", "user__email", "event__name")
    readonly_fields = ("id", "purchase_date", "qr_code_image")
