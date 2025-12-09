from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from catalogo.models import Obra
from usuarios.models import Usuario

estados = [
    ("En proceso", "En proceso"),
    ("Pagado", "Pagado"),
    ("Cancelado", "Cancelado")
]

metodos_pago = [
    ("tarjeta", "Tarjeta de crédito/débito"),
    ("transferencia", "Transferencia bancaria"),
    ("efectivo", "Pago en efectivo"),
    ("mercadopago", "MercadoPago"),
]

class BoletaDeCompra(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Cliente")
    direccion = models.CharField(max_length=100)
    monto = models.IntegerField(validators=[MinValueValidator(0)], verbose_name = "Monto")
    estado = models.CharField(max_length = 50, default = "En proceso", choices = estados, verbose_name = "Estado del producto")
    lista_productos = models.ManyToManyField(Obra, verbose_name="Lista de productos del pedido")

    metodo_pago = models.CharField(max_length=50, choices=metodos_pago, blank=True, verbose_name="Método de pago seleccionado")
    # Proveedor que hará el pago (para futuro)
    proveedor_pago = models.CharField(max_length=50, blank=True, verbose_name="Proveedor de pago")
    id_sesion_pago = models.CharField(max_length=200, blank=True, verbose_name="ID de sesión del proveedor de pago")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    ult_actualizado = models.DateTimeField(auto_now=True, verbose_name="Última vez actualizado")