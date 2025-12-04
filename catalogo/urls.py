from django.urls import path
from . import views

urlpatterns = [
    path('lienzo/', views.catalogo_lienzo, name = "lienzo"),
    path('impresiones/', views.catalogo_impresiones, name = "impresiones"),
    path('murales/', views.catalogo_murales, name = "murales"),
    path('obras/<int:obra_id>', views.detalles, name = "obra"),
]