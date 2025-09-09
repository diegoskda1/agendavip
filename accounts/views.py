from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm

# ------------------------------
# Registro de usuário
# ------------------------------
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            login(request, user)
            return redirect('home')  # substitua 'home' pela sua view inicial
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/register.html', context)

# ------------------------------
# Login de usuário
# ------------------------------
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo {user.full_name}!')
            # Redireciona de acordo com tipo de usuário
            if user.user_type == 'organizer':
                return redirect('organizer_dashboard')
            elif user.user_type == 'admin':
                return redirect('admin:index')
            else:
                return redirect('home')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
    return render(request, 'accounts/login.html')

# ------------------------------
# Logout de usuário
# ------------------------------
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('home')

# ------------------------------
# Editar perfil de usuário
# ------------------------------
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)
