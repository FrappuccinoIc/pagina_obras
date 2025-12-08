from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from catalogo.models import Obra
from usuarios.models import Usuario

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

@login_required
def quitar_de_carrito(req):
    if req.method == 'POST':
        obra_id = req.POST.get('obra')

        lista_productos = req.session.get("carrito", [])
        if obra_id in lista_productos:
            lista_productos.remove(obra_id)
            req.session["carrito"] = lista_productos
        
        obras = Obra.objects.filter(id__in=lista_productos).order_by("id")
        total = sum(obra.precio for obra in obras)
        html = f"""
            <div id="cart-total" hx-swap-oob="true">
                Total: ${total}
            </div>

            <div id="empty-message" class="text-muted" hx-swap-oob="true">
                {"<h4>No hay obras en la lista.</h4>" if not lista_productos else ""}
            </div>

            <input type="submit" id="boton-pago" class="btn btn-success w-100 mt-3" hx-swap-oob="true" {"disabled" if not lista_productos else ""} value="Proceder al Pago">
        """

        return HttpResponse(html)
    
@login_required
def checkout(req):
    lista_productos = req.session.get("carrito", [])
    try: usuario = Usuario.objects.get()
    except: return redirect(reverse("restringido"))
    return render(req, "checkout/checkout.html")