from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from catalogo.models import Obra

@login_required
def carrito(req):
    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito).order_by("id")
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

def quitar_de_carrito(req):
    if req.method == 'POST':
        obra_id = req.POST.get('obra')

        lista_productos = req.session.get("carrito", [])
        print(lista_productos)
        if obra_id in lista_productos:
            lista_productos.remove(obra_id)
            req.session["carrito"] = lista_productos
        print(lista_productos)
        
        obras = Obra.objects.filter(id__in=lista_productos).order_by("id")
        total = sum(obra.precio for obra in obras)
        print(obras, total)
        html = f"""
            <div id="cart-total" hx-swap-oob="true">
                Total: ${total}
            </div>

            <div id="empty-message" class="text-muted" hx-swap-oob="true">
                {"<h4>No hay obras en la lista.</h4>" if not lista_productos else ""}
            </div>
        """

        return HttpResponse(html)