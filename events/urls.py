from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # lista de eventos
    path('', views.EventListView.as_view(), name='event_list'),

    # detalhe de evento (use pk ou slug, escolha um)
    path('<int:pk>/', views.event_detail, name='event_detail'),

    # lista de locais
    path('venues/', views.VenueListView.as_view(), name='venue_list'),

    # lista de artistas
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),

    # sobre
    path('sobre/', views.about, name='about'),

    # Politica de privacidade
    path('privacidade/', views.privacy_policy, name='privacy_policy'),

    # termos de uso
    path('termos/', views.terms_of_use, name='terms_of_use'),
    
    #buscar
    path('search/', views.search_events, name='search_events'),

]
