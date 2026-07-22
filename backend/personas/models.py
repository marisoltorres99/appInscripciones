from django.conf import settings
from django.db import models


class Alumno(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumno',
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'


class Profesor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesor',
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'
