from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from catalogo.models import Obra
from usuarios.models import Usuario
from django.contrib.auth.models import User
from .forms import MetodoPagoForm
from .models import BoletaDeCompra

def verificar_disponibilidad_obras(req, obras, carrito):
    modificado = False
    for obra in obras:
        if obra.estado != "Disponible":
            try:
                carrito.remove(f"{obra.id}")
                modificado = True
                obras = obras.exclude(id = obra.id)
            except: pass
    if modificado:
        req.session["carrito"] = carrito

    return {"obras": obras, "carrito": carrito}

@login_required
def carrito(req):
    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito).order_by("id")
    obj = verificar_disponibilidad_obras(req, obras, obras_id_carrito)
    obras = obj["obras"]
    obras_id_carrito = obj["carrito"]

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
    if req.method != "POST": return redirect(reverse("ver_carrito"))

    try: usuario = Usuario.objects.get(cuenta__id = req.user.id)
    except: return redirect(reverse("restringido"))

    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito).order_by("id")

    if(len(obras_id_carrito) == 0):
        return render(req, "checkout/checkout.html", {
            "usuario": usuario,
            "obras": obras,
            "monto_total": 0
        })

    obj = verificar_disponibilidad_obras(req, obras, obras_id_carrito)
    obras = obj["obras"]
    obras_id_carrito = obj["carrito"]

    monto_total = sum(obra.precio for obra in obras)

    if(len(obras_id_carrito) == 0): return redirect(reverse("ver_carrito"))
    
    return render(req, "checkout/checkout.html", {
        "usuario": usuario,
        "lista_productos": obras,
        "monto_total": monto_total
    })

@login_required
def quitar_en_checkout(req):
    if req.method == 'POST':
        producto_id = req.POST.get('producto')

        lista_productos = req.session.get("carrito", [])
        if producto_id in lista_productos:
            lista_productos.remove(producto_id)
            req.session["carrito"] = lista_productos
        
        obras = Obra.objects.filter(id__in=lista_productos).order_by("id")
        total = sum(obra.precio for obra in obras)
        html = f"""
            <h2 id="cart-total" class="row text-center border-top mt-2 pt-3" hx-swap-oob="true">Total: { total }$</h2>

            <div id="empty-message" class="text-muted mb-3" hx-swap-oob="true">
                {"<h4>No hay productos en la lista.</h4>" if not lista_productos else ""}
            </div>

            <input id="boton-pago" type="submit" class="btn btn-primary row" hx-swap-oob="true" {"disabled" if not lista_productos else ""} value="Ir al siguiente paso >">
        """

        return HttpResponse(html)

@login_required
def metodo_pago(req):
    if req.method != "POST": return redirect(reverse("ver_carrito"))

    usuario = Usuario.objects.get(cuenta__id = req.user.id)
    direccion = req.POST.get('texto-direccion')
    if not direccion: return redirect(reverse("ver_carrito"))
    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito).order_by("id")

    obj = verificar_disponibilidad_obras(req, obras, obras_id_carrito)
    obras = obj["obras"]
    obras_id_carrito = obj["carrito"]

    if(len(obras_id_carrito) == 0): return redirect(reverse("ver_carrito"))

    metodo_pago_form = MetodoPagoForm()
        
    return render(req, "checkout/metodo_pago.html", {"usuario": usuario, "direccion": direccion, "metodo_pago_form": metodo_pago_form})

@login_required
def finalizar(req):
    if req.method != "POST": return redirect(reverse("restringido"))
    usuario = Usuario.objects.get(cuenta__id = req.user.id)
    direccion = req.POST.get('direccion')
    if not direccion: 
        print(direccion)
        return redirect(reverse("ver_carrito"))

    obras_id_carrito = req.session.get("carrito", [])
    obras = Obra.objects.filter(id__in = obras_id_carrito).order_by("id")
    print(obras_id_carrito, obras)
    for obra in obras:
        print(obra, obra.id, type(obra.id), f"{obra.id}" in obras_id_carrito)
        if obra.estado != "Disponible": return redirect(reverse("restringido"))
        obras_id_carrito.remove(f"{obra.id}")
        if obra.medio != "Impresiones": 
            obra.estado = "Agotado"
        obra.save()
    req.session["carrito"] = obras_id_carrito
    metodo_pago = req.POST.get('metodo_pago')
    boleta = BoletaDeCompra.objects.create(
        cliente = usuario,
        direccion = direccion,
        monto = sum(obra.precio for obra in obras),
        estado = "Pagado",
        metodo_pago = metodo_pago
    )
    boleta.lista_productos.set(obras)
    boleta.save()

    return render(req, 'checkout/finalizar_compra.html', {"boleta": boleta})