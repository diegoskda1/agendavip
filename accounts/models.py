from django.contrib.auth.models import AbstractUser
from django.db import models

# Tipos de usuário possíveis
USER_TYPE_CHOICES = (
    ('customer', 'Cliente'),
    ('organizer', 'Organizador'),
    ('admin', 'Administrador'),
)

class CustomUser(AbstractUser):
    """
    Usuário customizado do AgendaVIP.
    Serve como base para integração com PagSeguro e controle de acesso.
    """
    full_name = models.CharField(max_length=150, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer', verbose_name="Tipo de Usuário")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    USERNAME_FIELD = 'email'   # login via email
    REQUIRED_FIELDS = ['username', 'full_name']  # username ainda é obrigatório

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"


class Profile(models.Model):
    """
    Perfil opcional para armazenar informações extras do usuário.
    Pode ser usado para endereços, preferências de eventos, histórico, etc.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")
    zipcode = models.CharField(max_length=20, blank=True, null=True, verbose_name="CEP")
    newsletter = models.BooleanField(default=True, verbose_name="Receber Newsletter")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"Perfil de {self.user.full_name}"
