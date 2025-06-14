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
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.conf import settings
from conversor import db_to_csv, reviews_to_csv

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
# ---------- Vista de estadísticas ----------
@login_required
def estadisticas_view(request):
    """Muestra gráficas simples generadas a partir del CSV exportado."""
    csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    reviews_path = settings.MEDIA_ROOT / 'reviews.csv'
    if (not csv_path.exists() or csv_path.stat().st_size == 0 or
            not reviews_path.exists() or reviews_path.stat().st_size == 0):
        db_to_csv(csv_path)
        reviews_to_csv(reviews_path)

    # Solo una lectura de pandas
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()
    try:
        df_reviews = pd.read_csv(reviews_path)
    except pd.errors.EmptyDataError:
        df_reviews = pd.DataFrame()
    df['generos'] = df['generos'].str.split(',')
    df_gen = df.explode('generos')

    genero_counts = df_gen['generos'].value_counts()
    usuario_counts = df_reviews.set_index('usuario__username')['count']
    top_user = usuario_counts.idxmax() if not usuario_counts.empty else 'N/A'
    top_user_count = int(usuario_counts.max()) if not usuario_counts.empty else 0
    genero_mas = genero_counts.idxmax() if not genero_counts.empty else 'N/A'
    genero_mas_count = int(genero_counts.max()) if not genero_counts.empty else 0
    genero_menos = genero_counts.idxmin() if not genero_counts.empty else 'N/A'
    genero_menos_count = int(genero_counts.min()) if not genero_counts.empty else 0

    if 'calificacion_media' in df.columns and not df.empty:
        best_idx = df['calificacion_media'].idxmax()
        book_best = df.loc[best_idx, 'nombre']
        book_best_count = int(df.loc[best_idx, 'calificaciones_count']) if 'calificaciones_count' in df.columns else 0
        worst_idx = df['calificacion_media'].idxmin()
        book_worst = df.loc[worst_idx, 'nombre']
        book_worst_count = int(df.loc[worst_idx, 'calificaciones_count']) if 'calificaciones_count' in df.columns else 0
    else:
        book_best = 'N/A'
        book_best_count = 0
        book_worst = 'N/A'
        book_worst_count = 0

    # Gráfico de géneros
    fig1, ax1 = plt.subplots()
    genero_counts.plot(kind='bar', ax=ax1, color=plt.cm.Paired.colors)
    ax1.set_xlabel('Género')
    ax1.set_ylabel('Cantidad de libros')
    ax1.set_title('Libros por género')
    img1 = BytesIO()
    fig1.tight_layout()
    fig1.savefig(img1, format='png')
    plt.close(fig1)
    img1.seek(0)
    grafico_genero = base64.b64encode(img1.read()).decode('utf-8')

    # Gráfico de calificaciones por libro
    fig2, ax2 = plt.subplots()
    if 'calificacion_media' in df.columns:
        colores = plt.cm.tab20.colors[:len(df)]
        df.sort_values('calificacion_media', ascending=False).set_index('nombre')['calificacion_media'].plot(kind='bar', ax=ax2, color=colores)
    ax2.set_xlabel('Libro')
    ax2.set_ylabel('Calificación promedio')
    ax2.set_title('Calificación media por libro')
    fig2.tight_layout()
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    plt.close(fig2)
    img2.seek(0)
    grafico_calificacion = base64.b64encode(img2.read()).decode('utf-8')

    # Gráfico de reseñas por usuario
    fig3, ax3 = plt.subplots()
    usuario_counts.plot(kind='bar', ax=ax3, color=plt.cm.viridis.colors)
    ax3.set_xlabel('Usuario')
    ax3.set_ylabel('Cantidad de reseñas')
    ax3.set_title('Reseñas por usuario')
    fig3.tight_layout()
    img3 = BytesIO()
    fig3.savefig(img3, format='png')
    plt.close(fig3)
    img3.seek(0)
    grafico_usuarios = base64.b64encode(img3.read()).decode('utf-8')

    context = {
        'genero_mas': genero_mas,
        'genero_mas_count': genero_mas_count,
        'genero_menos': genero_menos,
        'genero_menos_count': genero_menos_count,
        'book_best': book_best,
        'book_best_count': book_best_count,
        'book_worst': book_worst,
        'book_worst_count': book_worst_count,
        'top_user': top_user,
        'top_user_count': top_user_count,
        'grafico_genero': grafico_genero,
        'grafico_calificacion': grafico_calificacion,
        'grafico_usuarios': grafico_usuarios,
    }
    return render(request, 'libros/estadisticas.html', context)