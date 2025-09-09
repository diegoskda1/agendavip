from django.contrib import admin
from django.urls import path, include
from .views import HomeView  # importar a view corretamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', HomeView.as_view(), name='home'),  # usar a view aqui
]
