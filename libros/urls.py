from django.urls import path
from .views import AutorListCreateView, LibroListCreateView, GeneroListCreateView, CalificacionUsuarioListCreateView

urlpatterns = [
    path('autores/', AutorListCreateView.as_view(), name='lista_crear_autor'),
    path('libros/', LibroListCreateView.as_view(), name='lista_crear_libro'),
    path('generos/', GeneroListCreateView.as_view(), name='genero_list_create'),
    path('calificaciones/', CalificacionUsuarioListCreateView.as_view(), name='calificacion_list_create')
]