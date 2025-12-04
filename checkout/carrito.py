from decimal import Decimal
from django.conf import settings
from catalogo.models import Obra

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(settings.CART_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CART_SESSION_ID] = {}
        self.carrito = carrito

    def agregar(self, obra, cantidad=1):
        obra_id = str(obra.id)
        if obra_id not in self.carrito:
            self.carrito[obra_id] = {
                'cantidad': 0,
                'precio': str(obra.precio)
            }
        self.carrito[obra_id]['cantidad'] += cantidad
        self.session.modified = True

    def eliminar(self, obra):
        obra_id = str(obra.id)
        if obra_id in self.carrito:
            del self.carrito[obra_id]
            self.session.modified = True

    def actualizar_cantidad(self, obra, cantidad):
        obra_id = str(obra.id)
        if obra_id in self.carrito:
            self.carrito[obra_id]['cantidad'] = cantidad
            self.session.modified = True

    def limpiar(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def __iter__(self):
        obra_ids = self.carrito.keys()
        obras = Obra.objects.filter(id__in=obra_ids)

        for obra in obras:
            item = self.carrito[str(obra.id)]
            item['obra'] = obra
            item['subtotal'] = Decimal(item['precio']) * item['cantidad']
            yield item

    def total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())
