from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogo.models import Obra

@login_required
def carrito(req):
    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito)
    modificado = False
    for obra in obras:
        if obra.estado != "Disponible":
            try:
                obras_id_carrito.remove(f"{obra.id}")
                modificado = True
                obras = obras.exclude(id = obra.id)
            except: pass
    if modificado:
        req.session["carrito"] = obras_id_carrito
        print(req.session.get("carrito", []))
    monto_total = 0
    for obra in obras:
        monto_total += obra.precio
    return render(req, "checkout/carrito.html", {"obras": obras, "monto_total": monto_total, "carrito": obras_id_carrito})