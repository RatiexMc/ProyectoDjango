from django.urls import path
from .views import AutorListCreateView, LibroListCreateView

urlpatterns = [
    path('autores/', AutorListCreateView.as_view(), name='lista_crear_autor'),
    path('libros/', LibroListCreateView.as_view(), name='lista_crear_libro'),
]