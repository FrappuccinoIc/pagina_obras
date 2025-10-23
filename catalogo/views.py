from django.shortcuts import render
from .models import Obra
from django.core.paginator import Paginator

def catalogo_paginacion(req, medio):
    obra = Obra.objects.filter(medio = medio).order_by("id")
    pag = Paginator(obra, 12)

    page_number = req.GET.get('page') # Se pasa la url que se quiere conseguir, en este caso: ?page=n
    page_obj = pag.get_page(page_number)

    # 🔹 Rango de páginas visibles (ejemplo: 5)
    index = page_obj.number - 1  # Índice actual. Paginator.number nos da un número indexeado a 1, no a 0. Se resta para mantener una indexación de 0 para el rango
    max_index = len(pag.page_range) # Consigue la cantidad de paginas en relación con la cantidad de objetos por página
    start_index = max(index - 2, 0)
    end_index = min(index + 3, max_index)
    page_range = pag.page_range[start_index:end_index]

    return [page_obj, page_range]

def catalogo_lienzo(req):
    medio = "Lienzo"
    obj_return = catalogo_paginacion(req, medio)
    page_obj = obj_return[0]
    page_range = obj_return[1]

    return render(req, 'catalogo/catalogo.html', {
        "medio": medio,
        "page_obj": page_obj,
        "page_range": page_range, 
    })

def catalogo_impresiones(req):
    medio = "Impresiones"
    obj_return = catalogo_paginacion(req, medio)
    page_obj = obj_return[0]
    page_range = obj_return[1]

    return render(req, 'catalogo/catalogo.html', {
        "medio": medio,
        "page_obj": page_obj,
        "page_range": page_range, 
    })

def detalles(req, obra_id):
    obra = Obra.objects.get(id = obra_id)
    return render(req, 'catalogo/detalles.html', {"obra": obra})