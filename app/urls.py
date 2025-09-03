from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('cart/', include('cart.urls', namespace='cart')),
    path("payments/", include("payments.urls", namespace="payments")),
    path("tickets/", include("tickets.urls", namespace="tickets")),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)