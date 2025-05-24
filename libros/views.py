from django.shortcuts import render, redirect
from .forms import LibroForm, CalificacionForm 
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Autor, Libro, Genero, CalificacionUsuario
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionUsuarioSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Vistas API
class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    
class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class CalificacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# Vista para subir libros (HTML)
@login_required
def subir_libro(request):
    libro = None
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save()
            mensaje = "¡Libro subido correctamente!"
    else:
        form = LibroForm()

    return render(request, 'libros/subir_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

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

# Nueva vista: Biblioteca de libros (HTML)
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
@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    messages.success(request, "Libro eliminado correctamente.")
    return redirect('biblioteca_libros')

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
@login_required
def ver_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    reseñas = CalificacionUsuario.objects.filter(libro=libro).order_by('-fecha')
    return render(request, 'libros/ver_libro.html', {
        'libro': libro,
        'reseñas': reseñas
    })
