from django import forms

lista_metodos = [
    ("tarjeta", "Tarjeta de crédito/débito"),
    ("transferencia", "Transferencia bancaria"),
    ("efectivo", "Pago en efectivo"),
    ("mercadopago", "MercadoPago"),
]

class MetodoPagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(choices=[
    ("tarjeta", "Tarjeta de crédito/débito"),
    ("transferencia", "Transferencia bancaria"),
    ("efectivo", "Pago en efectivo"),
    ("mercadopago", "MercadoPago"),
], required=False, label="Método de pago seleccionado")