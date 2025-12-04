from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:obra_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:obra_id>/', views.eliminar_item, name='eliminar_item'),
    path('carrito/actualizar/<int:obra_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
]
