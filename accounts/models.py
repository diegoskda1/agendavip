from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    full_name = models.CharField("Nome Completo", max_length=150)
    cpf = models.CharField("CPF", max_length=11, unique=True, validators=[RegexValidator(r'^\d{11}$', "Digite um CPF válido com 11 números (somente números).")])
    phone = models.CharField("Telefone/WhatsApp", max_length=20)
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)

    def __str__(self):
        return self.username
