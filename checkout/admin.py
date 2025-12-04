from django.contrib import admin
from .models import BoletaDeCompra

class BoletaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente_nombre', 'get_cliente_apellidos', 'fecha_creacion', 'ult_actualizado')
    readonly_fields = ('fecha_creacion', 'ult_actualizado')

    def get_cliente_nombre(self, obj): return obj.cliente.nombre

    get_cliente_nombre.admin_order_field = 'cliente__nombre'
    get_cliente_nombre.short_description = 'Nombre del cliente'

    def get_cliente_apellidos(self, obj): return obj.cliente.apellidos

    get_cliente_apellidos.admin_order_field = 'cliente__apellidos'
    get_cliente_apellidos.short_description = 'Apellido Paterno del cliente'

admin.site.register(BoletaDeCompra, BoletaAdmin)