from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('catalogo/', include("catalogo.urls")),
    path('carrito/', include("checkout.urls")),
    path('usuarios/', include("usuarios.urls")),
    path('info/', views.info, name = "info"),
    path('pedidos/', views.pedidos, name = "pedidos"),
    path('admin/', admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)