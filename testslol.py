from django import forms

metodos_pago = [
    ("tarjeta", "Tarjeta de crédito/débito"),
    ("transferencia", "Transferencia bancaria"),
    ("efectivo", "Pago en efectivo"),
    ("mercadopago", "MercadoPago"),
]

class MetodoPagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(
        choices=metodos_pago,
        required=False,
        label="Método de pago seleccionado"
    )

form = MetodoPagoForm()
print(form.as_p())
