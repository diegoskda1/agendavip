from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Admin do CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'full_name', 'user_type', 'is_staff', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active', 'groups']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'full_name', 'password', 'cpf', 'phone', 'user_type')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'full_name', 'cpf', 'phone', 'user_type',
                'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions'
            )
        }),
    )

    search_fields = ('email', 'full_name', 'username', 'cpf')
    ordering = ('email',)


# Admin do Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'zipcode', 'newsletter']
    search_fields = ['user__full_name', 'user__email', 'city', 'state', 'zipcode']
    list_filter = ['newsletter', 'state']

# Registrar no admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
