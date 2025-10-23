from django.contrib import admin
from .models import Etiqueta, Obra

class EtiquetaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')
class ObraAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(Etiqueta,EtiquetaAdmin)
admin.site.register(Obra,ObraAdmin)