from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'fecha_lanzamiento', 'generos', 'archivo']
        widgets = {
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'}),
        }
