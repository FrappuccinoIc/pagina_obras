from django.contrib import admin
from django.urls import path
from django.conf import settings

from core import views as views_core
from catalogo import views as views_catalogo

urlpatterns = [
    path('', views_core.home, name = 'home'),
    path('lienzo/', views_catalogo.catalogo_lienzo, name = "lienzo"),
    path('impresiones/', views_catalogo.catalogo_impresiones, name = "impresiones"),
    path('murales/', views_catalogo.catalogo_murales, name = "murales"),
    path('info/', views_core.info, name = "info"),
    path('pedidos/', views_core.pedidos, name = "pedidos"),
    path('carrito/', views_core.carrito, name = "carrito"),
    path('obras/<int:obra_id>', views_catalogo.detalles, name = "obra"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)