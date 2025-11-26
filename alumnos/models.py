from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnos')
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Email del Alumno")
    curso = models.CharField(max_length=100, verbose_name="Curso")
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación", null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_completo} - {self.curso}"