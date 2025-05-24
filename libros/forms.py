from django import forms
from .models import Libro, CalificacionUsuario

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'fecha_lanzamiento', 'generos', 'archivo']
        widgets = {
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'}),
        }
class CalificacionForm(forms.ModelForm):
    class Meta:
        model = CalificacionUsuario
        fields = ['resenia', 'calificacion']
        widgets = {
            'resenia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }