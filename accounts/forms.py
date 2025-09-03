from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import User


def validar_cpf(cpf: str) -> bool:
    """Valida um CPF de acordo com os dígitos verificadores"""
    cpf = ''.join(filter(str.isdigit, cpf))  # remove tudo que não for número

    if len(cpf) != 11:
        return False

    # Elimina CPFs inválidos conhecidos (todos dígitos iguais)
    if cpf in [s * 11 for s in "0123456789"]:
        return False

    # Validação do 1º dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        return False

    # Validação do 2º dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf[10]):
        return False

    return True


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'cpf', 'email', 'phone', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not validar_cpf(cpf):
            raise ValidationError("CPF inválido. Digite um CPF válido.")
        return cpf


class CustomUserChangeForm(UserChangeForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Selecione a data',
            }
        ),
        input_formats=['%d/%m/%Y'],
        required=True
    )

    class Meta:
        model = User
        fields = ['full_name', 'cpf', 'email', 'phone', 'birth_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not validar_cpf(cpf):
            raise ValidationError("CPF inválido. Digite um CPF válido.")
        return cpf
