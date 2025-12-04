from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Obra
from .carrito import Carrito

def carrito(req):
    return render(req, "checkout/carrito.html")

def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'carrito.html', {
        'carrito_items': list(carrito),
        'total': carrito.total()
    })

def agregar_al_carrito(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    carrito = Carrito(request)
    carrito.agregar(obra)
    return redirect('ver_carrito')

def eliminar_item(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    carrito = Carrito(request)
    carrito.eliminar(obra)
    return redirect('ver_carrito')

def actualizar_cantidad(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = Carrito(request)
    carrito.actualizar_cantidad(obra, cantidad)
    return redirect('ver_carrito')

def vaciar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('ver_carrito')

def checkout(request):
    carrito = Carrito(request)
    # Más adelante aquí pondrás proceso de pago
    return render(request, 'checkout.html')
