from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

# Formulário para criação de usuário (usado no admin e registro)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'username',
            'cpf',
            'phone',
            'user_type',
            'password1',
            'password2'
        ]
        labels = {
            'full_name': 'Nome Completo',
            'email': 'E-mail',
            'username': 'Nome de Usuário',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'user_type': 'Tipo de Usuário',
        }

# Formulário para alteração de usuário (usado no admin e perfil)
class CustomUserChangeForm(UserChangeForm):
    password = None  # Ocultar campo de senha no formulário de edição
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'username',
            'cpf',
            'phone',
            'user_type',
            'is_active',
            'is_staff'
        ]
        labels = {
            'full_name': 'Nome Completo',
            'email': 'E-mail',
            'username': 'Nome de Usuário',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'user_type': 'Tipo de Usuário',
            'is_active': 'Ativo',
            'is_staff': 'Staff',
        }

# Formulário para edição do perfil (Profile)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'address',
            'city',
            'state',
            'zipcode',
            'newsletter'
        ]
        labels = {
            'address': 'Endereço',
            'city': 'Cidade',
            'state': 'Estado',
            'zipcode': 'CEP',
            'newsletter': 'Receber Newsletter'
        }
