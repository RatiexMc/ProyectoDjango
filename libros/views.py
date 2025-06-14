# Imports básicos
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroForm, CalificacionForm 
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Autor, Libro, Genero, CalificacionUsuario
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionUsuarioSerializer
from django.db.models import Q
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated  # Protege las vistas API

# ------------------------ Vistas API protegidas ------------------------

# Listar y crear autores
class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    def perform_create(self, serializer):
        # Asocia el autor al usuario que realiza la creación
        serializer.save(creado_por=self.request.user)

# Listar y crear géneros
class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated]  # Requiere usuario autenticado

    def perform_create(self, serializer):
        # Asocia el género al usuario que realiza la creación
        serializer.save(creado_por=self.request.user)

# Listar y crear libros
class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Obtener, actualizar, eliminar libro
class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Listar y crear calificaciones de usuario
class CalificacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# Eliminar, actualizar, obtener autor por ID
class AutorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

# Eliminar, actualizar, obtener género por ID
class GeneroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

# Eliminar, actualizar, obtener calificación por ID
class CalificacionUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# ------------------------ Vistas HTML ------------------------

# Subir un nuevo libro (vista con formulario HTML)
@login_required
def subir_libro(request):
    libro = None
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        # Actualizamos queryset de autores y géneros
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

        if form.is_valid():
            libro = form.save()
            mensaje = "¡Libro subido correctamente!"
            form = LibroForm()  # Limpiamos formulario
    else:
        form = LibroForm()
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

    return render(request, 'libros/subir_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

# Calificar un libro (vista con formulario HTML)
@login_required
def calificar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.usuario = request.user
            calificacion.libro = libro
            calificacion.save()
            return redirect('ver_libro', pk=libro.id)
    else:
        form = CalificacionForm()

    return render(request, 'libros/calificar_libro.html', {
        'libro': libro,
        'form': form
    })

# Biblioteca de libros con buscador
@login_required
def biblioteca_libros(request):
    query = request.GET.get("q")
    if query:
        libros = Libro.objects.filter(
            Q(nombre__icontains=query) |
            Q(autor__nombre__icontains=query)
        )
    else:
        libros = Libro.objects.all()

    return render(request, 'libros/biblioteca_libros.html', {'libros': libros})

# Eliminar un libro
@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    messages.success(request, "Libro eliminado correctamente.")
    return redirect('biblioteca_libros')

# Editar un libro
@login_required
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            mensaje = "¡Libro actualizado correctamente!"
            return redirect('biblioteca_libros')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libros/editar_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

# Ver detalle del libro (con reseñas)
@login_required
def ver_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    reseñas = CalificacionUsuario.objects.filter(libro=libro).order_by('-fecha')
    return render(request, 'libros/ver_libro.html', {
        'libro': libro,
        'reseñas': reseñas
    })
