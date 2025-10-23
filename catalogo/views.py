from django.shortcuts import render
from .models import Obra

def catalogo(req):
    obras = Obra.objects.all()
    return render(req, 'catalogo/catalogo.html', {"obras": obras})

def detalles(req, obra_id):
    obra = Obra.objects.get(id = obra_id)
    #obra = get_object_or_404(Obra,id = obra_id)
    return render(req, 'catalogo/detalles.html', {"obra": obra})