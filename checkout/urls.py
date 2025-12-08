from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito, name='ver_carrito'),
    path('quitar_de_carrito/', views.quitar_de_carrito, name="quitar_de_carrito")
]
