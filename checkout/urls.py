from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito, name='ver_carrito'),
    # path('agregar/<int:obra_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    # path('eliminar/<int:obra_id>/', views.eliminar_item, name='eliminar_item'),
    # path('actualizar/<int:obra_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    # path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    # path('checkout/', views.checkout, name='checkout'),
]
