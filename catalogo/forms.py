from django import forms
from .models import Etiqueta, obras_medios, obras_estados
from django.core.validators import MinValueValidator

class PublicacionForm(forms.Form):
    titulo = forms.CharField(label = "Titulo", required = True, max_length = 50)
    imagen = forms.ImageField(required = True)
    precio = forms.IntegerField(label = "Precio", required = True, validators=[MinValueValidator(1)])
    medio = forms.ChoiceField(choices = [(None, "Selecciona medio de obra")] + obras_medios)
    estado = forms.ChoiceField(choices = [(None, "Selecciona estado del producto")] + obras_estados)
    descripcion = forms.CharField(label = "Descripción", 
        widget=forms.Textarea(attrs={
            "rows": 5,
            "class": "form-control"
        }))
    etiquetas = forms.ModelMultipleChoiceField(queryset = Etiqueta.objects.all(), widget=forms.CheckboxSelectMultiple, required = False)

    def clean_imagen(self):
        img = self.cleaned_data.get("imagen")

        if img.content_type not in ["image/jpeg", "image/png"]:
            raise forms.ValidationError("Solo se aceptan archivos jpeg y png.")

        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Capacidad de archivo sobrepasa 5MB.")

        return img
    
class PublicacionEditarForm(forms.Form):
    titulo = forms.CharField(label = "Titulo", required = True, max_length = 50)
    imagen = forms.ImageField(required = False)
    precio = forms.IntegerField(label = "Precio", required = True, validators=[MinValueValidator(1)])
    medio = forms.ChoiceField(choices = [(None, "Selecciona medio de obra")] + obras_medios)
    estado = forms.ChoiceField(choices = [(None, "Selecciona estado del producto")] + obras_estados)
    descripcion = forms.CharField(label = "Descripción", 
        widget=forms.Textarea(attrs={
            "rows": 5,
            "class": "form-control"
        }))
    etiquetas = forms.ModelMultipleChoiceField(queryset = Etiqueta.objects.all(), widget=forms.CheckboxSelectMultiple, required = False)

    def clean_imagen(self):
        img = self.cleaned_data.get("imagen")

        if img is None:
            return None

        if img.content_type not in ["image/jpeg", "image/png"]:
            raise forms.ValidationError("Solo se aceptan archivos jpeg y png.")

        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Capacidad de archivo sobrepasa 5MB.")

        return img