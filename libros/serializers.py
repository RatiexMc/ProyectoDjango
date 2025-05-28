from rest_framework import serializers
from .models import Autor, Libro, Genero, CalificacionUsuario
from django.contrib.auth.models import User
class AutorSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad', 'creado_por']


class GeneroSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Genero
        fields = ['id', 'nombre', 'creado_por']



class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(),source='autor', write_only=True)
    generos = GeneroSerializer(many=True, read_only=True)
    generos_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Genero.objects.all(), write_only=True,source='generos')
    archivo = serializers.FileField(use_url=True) 
    class Meta:
        model = Libro
        fields = ['id','nombre','autor','autor_id','fecha_lanzamiento','generos','generos_id','vistas','archivo']
class CalificacionUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)#Muestra el nombre del usuario
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),source='usuario', write_only=True)
    libro = serializers.StringRelatedField(read_only=True)
    libro_id = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all(),source='libro',write_only=True)

    class Meta:
        model = CalificacionUsuario
        fields = ['id','usuario','usuario_id','libro','libro_id','resenia','calificacion','fecha']
        





