from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'apellidos', 'direccion')


admin.site.register(Usuario, UsuarioAdmin)