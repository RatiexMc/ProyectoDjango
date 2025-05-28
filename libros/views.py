from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroForm, CalificacionForm 
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Autor, Libro, Genero, CalificacionUsuario
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionUsuarioSerializer
from django.db.models import Q
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated  # ← para proteger las vistas API

# ------------------------ Vistas API protegidas ------------------------

# Vista para listar y crear autores (requiere usuario autenticado)
class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)


# Vista para listar y crear géneros (requiere usuario autenticado)
class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Asociar el género al usuario que hizo la solicitud
        serializer.save(creado_por=self.request.user)

# Vista para listar y crear libros (vía API)
class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Vista para detalle de libro (obtener, actualizar o eliminar)
class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Vista para listar y crear calificaciones (API)
class CalificacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# Vistas para eliminar entidades por ID
class AutorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class GeneroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class CalificacionUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# ------------------------ Vistas HTML ------------------------

# Subir nuevo libro mediante formulario HTML
@login_required
def subir_libro(request):
    libro = None
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        # Refrescar los queryset para asegurarse de incluir valores nuevos
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

        if form.is_valid():
            libro = form.save()
            mensaje = "¡Libro subido correctamente!"
            form = LibroForm()  # Limpiar formulario tras éxito
    else:
        form = LibroForm()
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

    return render(request, 'libros/subir_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

# Calificar libro desde vista HTML
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

# Biblioteca principal de libros
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

# Eliminar libro por ID
@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    messages.success(request, "Libro eliminado correctamente.")
    return redirect('biblioteca_libros')

# Editar libro existente
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

# Ver detalle del libro con reseñas
@login_required
def ver_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    reseñas = CalificacionUsuario.objects.filter(libro=libro).order_by('-fecha')
    return render(request, 'libros/ver_libro.html', {
        'libro': libro,
        'reseñas': reseñas
    })
