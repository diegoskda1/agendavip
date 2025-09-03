from decimal import Decimal
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

# ===============================
# Tipo de Evento (Cinema, Teatro, Show...)
# ===============================
class EventType(models.Model):
    name = models.CharField("Tipo de Evento", max_length=50, unique=True)

    class Meta:
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Evento"

    def __str__(self):
        return self.name

# ===============================
# Gênero
# ===============================
class Genre(models.Model):
    name = models.CharField("Gênero", max_length=100, unique=True)

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

    def __str__(self):
        return self.name

# ===============================
# Local do Evento
# ===============================
class Venue(models.Model):
    name = models.CharField("Nome do Local", max_length=200)
    map_link = models.URLField("Link do Local no Mapa", blank=True)
    address = models.CharField("Endereço", max_length=300, blank=True)
    phone = models.CharField("Telefone de Contato", max_length=20, blank=True)
    website = models.URLField("Site", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    cover_image = models.ImageField("Foto do Local", upload_to='venue_covers/', blank=True)

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"

    def __str__(self):
        return self.name

# ===============================
# Artista
# ===============================
class Artist(models.Model):
    name = models.CharField("Nome do Artista", max_length=200)
    phone = models.CharField("Telefone de Contato", max_length=20, blank=True)
    website = models.URLField("Site", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    profile_image = models.ImageField("Foto do Artista", upload_to='artist_photos/', blank=True)

    class Meta:
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"

    def __str__(self):
        return self.name

# ===============================
# Evento (Modelo 'pai' sem campos de ingressos)
# ===============================
class Event(models.Model):
    # Campos principais
    name = models.CharField("Nome do Evento", max_length=200)
    original_name = models.CharField("Nome Original", max_length=200, blank=True)
    description = models.TextField("Descrição do Evento", blank=True)
    cover_image = models.ImageField("Imagem de Capa", upload_to='event_covers/')
    rating = models.DecimalField(
        "Avaliação", max_digits=3, decimal_places=1, default=0.0,
        help_text="Avaliação do evento de 0.0 a 5.0"
    )

    # Relacionamentos
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name="Tipo de Evento"
    )
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name="Local do Evento"
    )
    artists = models.ManyToManyField(
        Artist, blank=True, related_name='events', verbose_name="Artistas"
    )
    genres = models.ManyToManyField(
        Genre, blank=True, related_name='events', verbose_name="Gêneros"
    )

    # Ficha técnica
    director = models.CharField("Direção", max_length=200, blank=True)
    duration_minutes = models.PositiveIntegerField("Duração (minutos)", null=True, blank=True)
    distributor = models.CharField("Distribuidor", max_length=200, blank=True)
    country_of_origin = CountryField("País de Origem", blank=True)

    # Datas e horários
    start_time = models.DateTimeField("Hora de Início")
    end_time = models.DateTimeField("Hora de Encerramento", null=True, blank=True) 
    sales_start_time = models.DateTimeField("Início das Vendas", null=True, blank=True)

    # Venda e destaque
    is_featured = models.BooleanField("Destaque na Página Inicial", default=False)
    is_active = models.BooleanField("Ativo para vendas", default=True)
    # REMOVIDOS OS CAMPOS DE INGRESSOS E PREÇOS DO EVENTO

    # SEO
    slug = models.SlugField("URL Amigável", unique=True)

    # Controle
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def is_currently_active(self):
        """Retorna True se o evento estiver dentro do período válido e ativo"""
        if not self.is_active:  # valor do campo no banco
            return False
        reference_time = self.end_time or self.start_time
        return reference_time >= timezone.now()
       

    class Meta:
        ordering = ['start_time']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.start_time > timezone.now()
    
    def is_past(self):
        reference_time = self.end_time or self.start_time
        return reference_time < timezone.now()
    
    def can_sell(self):
        return self.is_currently_active() and not self.is_past()

    def is_sold_out(self):
        # Esta função precisa ser ajustada, pois tickets_available não existe mais aqui
        try:
            return self.event_seats.available_seats() == 0
        except EventSeats.DoesNotExist:
            return True


# ===============================
# Assentos do Evento (Modelo 'filho' com ingressos e preços)
# ===============================
class EventSeats(models.Model):
    event = models.OneToOneField(
        "Event",
        on_delete=models.CASCADE,
        related_name="event_seats",
        verbose_name="Evento"
    )
    # CAMPOS DE ASSENTOS
    total_seats = models.PositiveIntegerField("Total de Assentos", help_text="Quantidade total de assentos do local")
    vip_seats = models.PositiveIntegerField("Assentos VIP", default=0)
    normal_seats = models.PositiveIntegerField("Assentos Normais", default=0)
    openbar_seats = models.PositiveIntegerField("Assentos OpenBar", default=0)
    map_image = models.ImageField("Mapa do Local", upload_to="seat_maps/", blank=True, null=True)

    # CAMPOS DE PREÇOS (MOVEU PARA CÁ)
    price = models.DecimalField("Preço Ingresso Normal", max_digits=8, decimal_places=2, null=True, blank=True)
    price_vip = models.DecimalField("Preço Ingresso Vip", max_digits=8, decimal_places=2, null=True, blank=True)
    price_openbar = models.DecimalField("Preço Ingresso OpenBar", max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Assentos do Evento"
        verbose_name_plural = "Assentos dos Eventos"

    def __str__(self):
        return f"{self.event.name} - Total: {self.total_seats} (VIP: {self.vip_seats}, Normal: {self.normal_seats}, OpenBar: {self.openbar_seats})"

    def available_seats(self):
        return self.vip_seats + self.normal_seats + self.openbar_seats