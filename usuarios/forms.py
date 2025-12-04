from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label = "Sobrenombre de Usuario", required = True, max_length=50, min_length=3)
    password = forms.CharField(label = "Contraseña", required = True, widget=forms.PasswordInput, min_length=8, max_length=24)
    confirm_password = forms.CharField(label = "Confirmar Contraseña", required = True, widget=forms.PasswordInput, min_length=8, max_length=24)

    nombre = forms.CharField(label = "Nombre de usuario", required = True, max_length=50, min_length=4)
    apellidos = forms.CharField(label = "Apellidos", required = True, max_length=200, min_length=4)
    direccion = forms.CharField(label = "Dirección", required = True, max_length=100, min_length=4)