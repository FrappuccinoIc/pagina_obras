from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name = "registrar"),
    path('registrar/admin', views.registrar_admin, name = "registrar_admin"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('perfil/', views.perfil, name ='perfil'),
    path('perfil/eliminar/', views.eliminar_usuario, name ='eliminar_usuario'),
]