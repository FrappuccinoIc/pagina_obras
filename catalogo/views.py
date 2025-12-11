from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Obra, Publicacion
from django.core.paginator import Paginator
from .forms import PublicacionForm, PublicacionEditarForm

def catalogo(req):
    filtros = {}

    medio = req.GET.get('medio', None)
    lista_medios = [t[0] for t in Obra.medio.field.choices]

    estado = req.GET.get('estado', None)
    lista_estados = [t[0] for t in Obra.estado.field.choices]

    if medio in lista_medios:
        filtros["medio"] = medio
    if estado in lista_estados:
        filtros["estado"] = estado

    obras = Obra.objects.filter(**filtros).order_by("id")
    pag = Paginator(obras, 12)

    page_number = req.GET.get('page') # Se pasa la url que se quiere conseguir, en este caso: ?page=n
    page_obj = pag.get_page(page_number)

    index = page_obj.number - 1  # Índice actual. Paginator.number nos da un número indexeado a 1, no a 0. Se resta para mantener una indexación de 0 para el rango
    max_index = len(pag.page_range) # Consigue la cantidad de paginas en relación con la cantidad de objetos por página
    start_index = max(index - 2, 0)
    end_index = min(index + 3, max_index)
    page_range = pag.page_range[start_index:end_index]

    return render(req, 'catalogo/catalogo.html', {
        "lista_medios": lista_medios,
        "medio_seleccionado": medio,
        "lista_estados": lista_estados,
        "estado_seleccionado": estado,
        "page_obj": page_obj,
        "page_range": page_range
    })

def detalles(req, obra_id):
    obra = Obra.objects.get(id = obra_id)
    publicacion = Publicacion.objects.get(obra__id = obra_id)
    return render(req, 'catalogo/detalles.html', {"obra": obra, "publicacion": publicacion})

@login_required
def add_to_carrito(req):
    if req.method == 'POST':
        obra = req.POST.get('obra')

        product_list = req.session.get("carrito", [])
        if obra not in product_list:
            product_list.append(obra)
            req.session["carrito"] = product_list
    return HttpResponse("")

@permission_required('catalogo.add_obra', login_url="/restringido")
def registrar_obra(req):
    if req.method == 'POST':
        form = PublicacionForm(req.POST, req.FILES)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            etiquetas = form.cleaned_data['etiquetas']
            obra_creada = Obra.objects.create(
                titulo = form.cleaned_data['titulo'],
                imagen = form.cleaned_data['imagen'],
                medio = form.cleaned_data['medio'],
                estado = form.cleaned_data['estado'],
                precio = form.cleaned_data['precio']
            )
            obra_creada.etiquetas.set(etiquetas)
            obra_creada.save()
            post = Publicacion.objects.create(descripcion = descripcion, obra = obra_creada)
            post.save()
            return redirect(reverse('catalogo'))
    else: 
        form = PublicacionForm()

    return render(req, 'catalogo/registrar_obra.html', {'form': form})

@permission_required('catalogo.change_obra', login_url="/restringido")
def editar_obra(req, obra_id):
    try: 
        obra = Obra.objects.get(id = obra_id)
        post = Publicacion.objects.get(obra__id = obra_id)
    except: 
        return redirect(reverse('restringido'))
    
    if req.method == 'POST':
        form = PublicacionEditarForm(req.POST, req.FILES)
        if form.is_valid():
            post.descripcion = form.cleaned_data['descripcion']
            etiquetas = form.cleaned_data['etiquetas']

            obra.titulo = form.cleaned_data['titulo']
            obra.medio = form.cleaned_data['medio']
            obra.estado = form.cleaned_data['estado']
            obra.precio = form.cleaned_data['precio']
            if form.cleaned_data['imagen']: 
                obra.imagen = form.cleaned_data['imagen']
            else: pass
            obra.etiquetas.set(etiquetas)

            obra.save()
            post.save()
            return redirect(reverse('obra', args=[obra_id]))
    else: 
        form = PublicacionEditarForm(initial = {
            'titulo': obra.titulo,
            'medio': obra.medio,
            'estado': obra.estado,
            'precio': obra.precio,
            'descripcion': post.descripcion,
            'etiquetas': obra.etiquetas.all()
        })

    return render(req, 'catalogo/editar_obra.html', {'form': form, "obra": obra})

@permission_required('catalogo.delete_obra', login_url="/restringido")
def eliminar_obra(req, obra_id):
    try: 
        obra = Obra.objects.get(id = obra_id)
        publicacion = Publicacion.objects.get(obra__id = obra_id)
    except: 
        return redirect(reverse('restringido'))
    if req.method == "POST":
        publicacion.delete()
        obra.delete()
        return redirect(reverse('catalogo'))
    return render(req, "catalogo/eliminar_obra.html", {"obra": obra, "publicacion": publicacion})