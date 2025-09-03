from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.user_tickets, name="user_tickets"),
    path("meus-ingressos/", views.user_tickets, name="user_tickets"),
    path("meu-ingresso/<uuid:ticket_id>/", views.user_ticket_detail, name="user_ticket_detail"),
]
