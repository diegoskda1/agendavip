from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

# ------------------------------
# Formulário para registro público seguro
# ------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'username',
            'cpf',
            'phone',
            'password1',
            'password2',
        ]
        labels = {
            'full_name': 'Nome Completo',
            'email': 'E-mail',
            'username': 'Nome de Usuário',
            'cpf': 'CPF',
            'phone': 'Telefone',
        }

    # Validações de unicidade
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if CustomUser.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está em uso.")
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Este telefone já está em uso.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'  # força todos os novos usuários como cliente
        if commit:
            user.save()
        return user

# ------------------------------
# Formulário para alteração de usuário (admin ou perfil)
# ------------------------------
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
            'is_staff',
            'groups',
            'user_permissions',
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
            'groups': 'Grupos',
            'user_permissions': 'Permissões de Usuário',
        }

# ------------------------------
# Formulário para edição do perfil
# ------------------------------
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
