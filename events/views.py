from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone
from .models import Event, EventSeats, Venue, Artist

# ===============================
# Lista de todos os eventos
# ===============================
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['start_time']
    paginate_by = 10

    def get_queryset(self):
        """Retorna todos os eventos futuros (incluindo destaques)"""
        now = timezone.now()
        return Event.objects.all().order_by('-start_time')

    def get_context_data(self, **kwargs):
        """Adiciona os eventos em destaque no contexto para o carrossel"""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['featured_events'] = Event.objects.filter(
            start_time__gte=now,
            is_featured=True
        ).order_by('start_time')
        return context


# ===============================
# Detalhe do evento
# ===============================
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    try:
        # Acessa a informação de assentos através da relação de um-para-um
        seats = event.event_seats
        
        # Cria um objeto com todas as informações necessárias, buscando de 'seats'
        ticket_info = {
            'vip_seats': seats.vip_seats,
            'vip_price': seats.price_vip,
            'normal_seats': seats.normal_seats,
            'normal_price': seats.price,
            'openbar_seats': seats.openbar_seats,
            'openbar_price': seats.price_openbar,
            'map_image': seats.map_image,
        }
    except EventSeats.DoesNotExist:
        # Lida com o caso onde não há assentos cadastrados
        ticket_info = None

    genres = event.genres.all() if hasattr(event, 'genres') else []
    artists = event.artists.all() if hasattr(event, 'artists') else []

    full_stars = range(int(event.rating)) if event.rating else []
    half_star = (event.rating % 1) >= 0.5 if event.rating else False
    empty_stars = range(5 - len(full_stars) - (1 if half_star else 0))

    # 🔹 Nova flag para habilitar/desabilitar vendas
    can_buy = event.is_currently_active()  # usa o método que já criamos no model

    context = {
        'event': event,
        'ticket_info': ticket_info,
        'genres': genres,
        'artists': artists,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
        'can_buy': can_buy,
    }

    

    return render(request, 'events/event_detail.html', context)
# ===============================
# Busca de eventos
# ===============================
from django.db.models import Q

def search_events(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | 
            Q(venue__name__icontains=query) | 
            Q(artists__name__icontains=query)
        ).distinct()
    else:
        events = Event.objects.all()  # ou Event.objects.none() se quiser não mostrar nada

    return render(request, 'events/event_list.html', {
        'events': events,
        'query': query,
    })



# ===============================
# Listagem de locais
# ===============================
class VenueListView(ListView):
    model = Venue
    template_name = 'events/venue_list.html'
    context_object_name = 'venues'
    ordering = ['name']
    paginate_by = 10


# ===============================
# Listagem de artistas
# ===============================
class ArtistListView(ListView):
    model = Artist
    template_name = 'events/artist_list.html'
    context_object_name = 'artists'
    ordering = ['name']
    paginate_by = 10


# ===============================
# Sobre
# ===============================
def about(request):
    context = {
        'company_name': 'Sigma Inovações',
        'company_website': 'https://www.sigmainovacoes.online/',
        'project_name': 'AgendaVIP',
        'project_description': 'Seu guia exclusivo para os melhores eventos, shows e experiências. Nunca perca um momento especial.',
        'additional_info': 'Desenvolvemos soluções digitais personalizadas para impulsionar seu negócio e projetos como o AgendaVIP que conectam pessoas a eventos de qualidade.',
    }
    return render(request, 'events/about.html', context)


# ===============================
# Politica de privacidade
# ===============================
def privacy_policy(request):
    context = {
        'company_name': 'Sigma Inovações',
        'project_name': 'AgendaVIP',
    }
    return render(request, 'events/privacy_policy.html', context)


# ===============================
# Termos de uso
# ===============================
def terms_of_use(request):
    context = {
        'company_name': 'Sigma Inovações',
        'project_name': 'AgendaVIP',
    }
    return render(request, 'events/terms_of_use.html', context)



def home(request):
    events = Event.objects.all()  
    return render(request, 'events/event_list.html', {'events': events})
