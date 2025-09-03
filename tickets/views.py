from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Ticket

@login_required
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-purchase_date")
    return render(request, "tickets/user_tickets.html", {"tickets": tickets})

@login_required
def user_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, "tickets/user_ticket_detail.html", {"ticket": ticket})