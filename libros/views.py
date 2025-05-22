from django.shortcuts import render

from rest_framework import generics
from .models import Autor, Libro, Genero, CalificacionUsuario
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionUsuarioSerializer

class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

class CalificacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer




