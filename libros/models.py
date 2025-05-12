from django.db import models
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
class Libro(models.Model):
    CALIFICACIONES = [
        ('MB','Muy Bueno'),
        ('B','Bueno'),
        ('M','Malo'),
        ('MM','Muy Malo'),
    ]

    nombre = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    genero = models.CharField(max_length=100)
    calificacion = models.CharField(max_length=2, choices=CALIFICACIONES)
    vistas = models.PositiveIntegerField(default =2)
    url = models.URLField(help_text="Apunta al Home.html o alguna página")

    def __str__(self):
        return self.nombre