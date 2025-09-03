from django.contrib import admin
from django.utils.html import format_html
from .models import EventType, Genre, Venue, Artist, Event, EventSeats

# ===============================
# Admin EventType
# ===============================
@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ===============================
# Admin Genre
# ===============================
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ===============================
# Admin Venue
# ===============================
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'map_link')
    search_fields = ('name',)

# ===============================
# Admin Artist
# ===============================
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ===============================
# Inline para Assentos e Preços
# ===============================
class EventSeatsInline(admin.StackedInline):
    model = EventSeats
    verbose_name = "Assentos e Preços"
    verbose_name_plural = "Assentos e Preços"
    max_num = 1
    can_delete = False
    fieldsets = (
        (None, {
            'fields': (
                'total_seats', 'vip_seats', 'normal_seats', 'openbar_seats',
                'price', 'price_vip', 'price_openbar', 'map_image',
            ),
        }),
    )
    readonly_fields = ('map_preview',)

    def map_preview(self, obj):
        if obj.map_image:
            return format_html(
                '<img src="{}" style="width: 200px; height: auto; border: 1px solid #ccc;" />',
                obj.map_image.url
            )
        return "(Sem mapa)"
    
    map_preview.short_description = "Pré-visualização do Mapa"

# ===============================
# Admin Evento (sem campos de preço e ingressos no display)
# ===============================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventSeatsInline]

    list_display = (
        'name', 'event_type', 'start_time', 'is_featured', 'rating_display'
    )
    list_filter = ('event_type', 'is_featured', 'start_time')
    search_fields = ('name', 'original_name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('artists', 'genres')

    def rating_display(self, obj):
        full_stars = int(obj.rating)
        half_star = obj.rating - full_stars >= 0.5
        stars_html = '★' * full_stars
        if half_star:
            stars_html += '½'
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        stars_html += '☆' * empty_stars
        return stars_html
    rating_display.short_description = 'Avaliação'


from django.contrib import admin
from .models import Event
from cart.models import Coupon
from tickets.models import Ticket

# Admin de eventos
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'venue')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Limita eventos do produtor apenas ao próprio usuário
        if request.user.groups.filter(name='Producer').exists():
            return qs.filter(producer=request.user)
        return qs

# Admin de cupons
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'event')

# Admin de vendas de ingressos
class TicketSaleAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'buyer_cpf', 'ticket_type', 'event', 'price', 'purchase_date')
    list_filter = ('event', 'ticket_type')
    search_fields = ('buyer_name', 'buyer_cpf', 'buyer_phone')

