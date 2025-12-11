from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name = "catalogo"),
    path('obras/registrar', views.registrar_obra, name = "registrar_obra"),
    path('obras/<int:obra_id>', views.detalles, name = "obra"),
    path('obras/<int:obra_id>/editar', views.editar_obra, name = "editar_obra"),
    path('obras/<int:obra_id>/eliminar', views.eliminar_obra, name="eliminar_obra"),
    path('add_to_carrito/', views.add_to_carrito, name="add_to_carrito")
]