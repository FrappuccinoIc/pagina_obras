from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name = "registrar"),
    path('registrar/admin', views.registrar_admin, name = "registrar_admin"),
    path('perfil/', views.perfil, name ='perfil'),
    path('perfil/eliminar/', views.eliminar_usuario, name ='eliminar_usuario'),
]