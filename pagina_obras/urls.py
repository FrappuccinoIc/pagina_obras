from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from core import views as views_core

urlpatterns = [
    path('', views_core.home, name = 'home'),
    path('catalogo', include("catalogo.urls")),
    path('carrito', include("checkout.urls")),
    path('', include("usuarios.urls")),
    path('info/', views_core.info, name = "info"),
    path('pedidos/', views_core.pedidos, name = "pedidos"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)