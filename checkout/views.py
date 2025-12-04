from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Obra

def carrito(req):
    obras = Obra.objects.all()
    monto_total = 0
    for obra in obras:
        monto_total += obra.precio
    return render(req, "checkout/carrito.html", {"obras": obras, "monto_total": monto_total})