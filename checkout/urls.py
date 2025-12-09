from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('carrito', views.carrito, name='ver_carrito'),
    path('quitar_de_carrito/', views.quitar_de_carrito, name="quitar_de_carrito"),
    path('quitar_en_checkout/', views.quitar_en_checkout, name="quitar_en_checkout"),
]
