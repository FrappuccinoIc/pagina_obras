from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Etiqueta(models.Model):
    nombre = models.CharField(max_length = 15, verbose_name = "Nombre")

    created = models.DateTimeField(auto_now = True, verbose_name = "Fecha de creación")
    updated = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de edición")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self): return self.nombre

obras_medios = [
    ("Lienzo", "Lienzo"),
    ("Impresiones", "Impresiones")
]

obras_estados = [
    ("Normal", "Normal"),
    ("En Tendencia", "En Tendencia"),
    ("Destacado", "Destacado")
]
class Obra(models.Model):
    titulo = models.CharField(max_length = 50, verbose_name = "Titulo")
    imagen = models.ImageField(upload_to = "obras", null = True, blank = True, verbose_name = "Imagen")
    medio = models.CharField(max_length = 50, default = "Lienzo", choices = obras_medios, verbose_name = "Medio de Obra")
    etiquetas = models.ManyToManyField(Etiqueta, verbose_name = "etiquetas")
    precio = models.IntegerField(validators=[MinValueValidator(0)], verbose_name = "Precio")
    stock = models.IntegerField(default = 0, validators=[MinValueValidator(0)], verbose_name = "Stock")
    descripcion = models.TextField(null = True, blank = True, verbose_name = "Descripción")
    estado = models.CharField(max_length = 50, default = "Normal", choices = obras_estados, verbose_name = "Estado del producto")

    created = models.DateTimeField(auto_now = True, verbose_name = "Fecha de publicación")
    updated = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de edición")

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

    def __str__(self): return self.titulo