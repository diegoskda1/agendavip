from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

def register_view(request):
    success = False
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # cria o usuário e salva no DB
            login(request, user)  # loga automaticamente
            success = True
            form = CustomUserCreationForm()  # limpa o formulário
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'success': success})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

from tickets.models import Ticket  # adicionar no topo do arquivo

@login_required
def profile_view(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    # Pegando todos os tickets do usuário
    tickets = Ticket.objects.filter(user=request.user).order_by("-purchase_date")
    
    return render(request, 'accounts/profile.html', {'form': form, 'tickets': tickets})

