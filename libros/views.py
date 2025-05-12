from django.shortcuts import render

from rest_framework import generics
from .models import Autor, Libro
from .serializers import AutorSerializer, LibroSerializer

class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer





