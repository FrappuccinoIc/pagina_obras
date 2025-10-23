from django.shortcuts import render
from .models import Obra

def catalogo_lienzo(req):
    obras = Obra.objects.filter(medio = "Lienzo")
    return render(req, 'catalogo/catalogo.html', {"obras": obras, "medio": "Lienzo"})

def catalogo_impresiones(req):
    obras = Obra.objects.filter(medio = "Impresiones")
    return render(req, 'catalogo/catalogo.html', {"obras": obras, "medio": "Impresión"})

def detalles(req, obra_id):
    obra = Obra.objects.get(id = obra_id)
    #obra = get_object_or_404(Obra,id = obra_id)
    return render(req, 'catalogo/detalles.html', {"obra": obra})