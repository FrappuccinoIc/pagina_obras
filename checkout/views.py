from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Obra

def carrito(req):
    obras = Obra.objects.all()
    return render(req, "checkout/carrito.html", {"obras": obras})