from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("cadastrar/", views.register_view, name="register"),
    path("entrar/", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("perfil/", views.profile_view, name="profile"),
]
