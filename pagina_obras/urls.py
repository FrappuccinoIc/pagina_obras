from django.contrib import admin
from django.urls import path
from catalogo import views as views_catalogo
from django.conf import settings

urlpatterns = [
    path('obras', views_catalogo.catalogo, name = "catalogo"),
    path('obras/<int:obra_id>', views_catalogo.detalles, name = "obra"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)