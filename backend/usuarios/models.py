from django.contrib.auth.models import AbstractUser
from django.db import models


class Institucion(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    ROL_ADMIN = 'admin'
    ROL_ALUMNO = 'alumno'
    ROL_PROFESOR = 'profesor'
    ROL_CHOICES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_ALUMNO, 'Alumno'),
        (ROL_PROFESOR, 'Profesor'),
    ]

    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    institucion = models.ForeignKey(
        Institucion, on_delete=models.PROTECT, related_name='usuarios',
        null=True, blank=True,
    )

    def __str__(self):
        return self.email
