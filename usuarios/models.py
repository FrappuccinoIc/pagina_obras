from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Usuario(models.Model):
    username = models.CharField(max_length=40, verbose_name="Username")
    nombre = models.CharField(max_length=40, verbose_name="Nombre de usuario")
    apellidos = models.CharField(max_length=200, verbose_name="Apellidos")
    direccion = models.CharField(max_length=100)
    cuenta = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cuenta enlazada")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self): return self.username