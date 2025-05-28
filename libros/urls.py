from django.urls import path
from .views import AutorListCreateView, LibroListCreateView, LibroDetailView, GeneroListCreateView, CalificacionUsuarioListCreateView, subir_libro, biblioteca_libros, eliminar_libro, editar_libro, ver_libro, calificar_libro, AutorDetailView, GeneroDetailView, CalificacionUsuarioDetailView

urlpatterns = [
    path('autores/', AutorListCreateView.as_view(), name='lista_crear_autor'),
    path('libros/', LibroListCreateView.as_view(), name='lista_crear_libro'),
    path('libros/<int:pk>',LibroDetailView.as_view(),name='libro-detalle'),
    path('generos/', GeneroListCreateView.as_view(), name='genero_list_create'),
    path('calificaciones/', CalificacionUsuarioListCreateView.as_view(), name='calificacion_list_create'),
    path('subir/', subir_libro, name='subir_libro'),
    path('', biblioteca_libros, name='biblioteca_libros'),
    path('eliminar/<int:pk>/', eliminar_libro, name='eliminar_libro'),
    path('editar/<int:pk>/', editar_libro, name='editar_libro'),
    path('ver/<int:pk>/', ver_libro, name='ver_libro'),
    path('libros/<int:libro_id>/calificar/', calificar_libro, name='calificar_libro'),
    path('autores/<int:pk>/', AutorDetailView.as_view(), name='autor-detalle'),
    path('generos/<int:pk>/', GeneroDetailView.as_view(), name='genero-detalle'),
    path('calificaciones/<int:pk>/', CalificacionUsuarioDetailView.as_view(), name='calificacion-detalle'),


]