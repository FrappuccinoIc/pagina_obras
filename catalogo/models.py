from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import cloudinary.uploader

class Etiqueta(models.Model):
    nombre = models.CharField(max_length = 15, verbose_name = "Nombre")
    descripcion = models.CharField(max_length = 70, default = "", verbose_name = "Descripción")

    created = models.DateTimeField(auto_now = True, verbose_name = "Fecha de creación")
    updated = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de edición")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self): return self.nombre

obras_medios = [
    ("Lienzo", "Lienzo"),
    ("Mural", "Mural"),
    ("Impresiones", "Impresiones")
]

obras_estados = [
    ("Disponible", "Disponible"),
    ("Agotado", "Agotado"),
    ("Reservado", "Reservado")
]
class Obra(models.Model):
    titulo = models.CharField(max_length = 50, verbose_name = "Titulo")

    imagen = models.ImageField(upload_to = "obras/", null = True, blank = True, verbose_name = "Imagen")
    imagen_url = models.URLField(blank=True, null=True)

    medio = models.CharField(max_length = 50, default = "Lienzo", choices = obras_medios, verbose_name = "Medio de Obra")
    etiquetas = models.ManyToManyField(Etiqueta, verbose_name = "etiquetas")
    precio = models.IntegerField(validators=[MinValueValidator(0)], verbose_name = "Precio")
    estado = models.CharField(max_length = 50, default = "Normal", choices = obras_estados, verbose_name = "Estado del producto")

    created = models.DateTimeField(auto_now = True, verbose_name = "Fecha de creación")
    updated = models.DateTimeField(auto_now_add = True, verbose_name = "Última vez editado")

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

    def save(self, *args, **kwargs):
        # Si se cargó una imagen local nueva:
        if self.imagen:
            upload = cloudinary.uploader.upload(self.imagen)
            self.imagen_url = upload.get("secure_url")   # ← Guardamos solo la URL
            self.imagen = None                   # opcional: ya no la guardas local

        super().save(*args, **kwargs)

    def __str__(self): return self.titulo

fuentes_de_texto = [
    ("base", "base"),
    ("oswald", "oswald")
]

class Publicacion(models.Model):
    descripcion = models.TextField(null = True, blank = True, verbose_name = "Descripción")
    fuente_de_texto = models.CharField(max_length=20, choices=fuentes_de_texto, default="base", verbose_name="Fuente de texto")
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, verbose_name="Cita de publicación")

    created = models.DateTimeField(auto_now = True, verbose_name = "Fecha de creación")
    updated = models.DateTimeField(auto_now_add = True, verbose_name = "Última vez editado")

    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"