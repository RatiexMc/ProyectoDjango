from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    generos = models.ManyToManyField(Genero)  # Relación M:N con género
    vistas = models.PositiveIntegerField(default=2)
    archivo = models.FileField(
    upload_to='libros/',
    validators=[FileExtensionValidator(allowed_extensions=['epub'])],
    help_text="Solo archivos EPUB"
    )


    def __str__(self):
        return self.nombre

class CalificacionUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones_usuario')
    resenia = models.TextField(blank=True)
    calificacion = models.PositiveSmallIntegerField()  # Por ejemplo: 1=malo a 5=muy bueno
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.nombre} ({self.calificacion})"