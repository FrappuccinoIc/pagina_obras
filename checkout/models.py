from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from catalogo.models import Obra
from usuarios.models import Usuario

obras_estados = [
    ("En proceso", "En proceso"),
    ("Entregado", "Entregado"),
    ("Cancelado", "Cancelado")
]
class BoletaDeCompra(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Cliente")
    monto = models.IntegerField(validators=[MinValueValidator(0)], verbose_name = "Monto")
    estado = models.CharField(max_length = 50, default = "En proceso", choices = obras_estados, verbose_name = "Estado del producto")
    lista_productos = models.ManyToManyField(Obra, verbose_name="Lista de productos del pedido")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    ult_actualizado = models.DateTimeField(auto_now=True, verbose_name="Última vez actualizado")