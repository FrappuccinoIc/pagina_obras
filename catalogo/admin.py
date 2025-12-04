from django.contrib import admin
from .models import Etiqueta, Obra, Publicacion

class EtiquetaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class ObraAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class PublicacionAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
    list_display=('get_obra_titulo', 'created')

    @admin.display(description='Titulo de obra', ordering='obra__titulo')
    def get_obra_titulo(self, obj):
        return obj.obra.titulo


admin.site.register(Etiqueta,EtiquetaAdmin)
admin.site.register(Obra,ObraAdmin)
admin.site.register(Publicacion,PublicacionAdmin)