from django.db import models

from academico.models import Clase
from personas.models import Alumno


class Inscripcion(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_FINALIZADA = 'finalizada'
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_CANCELADA, 'Cancelada'),
        (ESTADO_FINALIZADA, 'Finalizada'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, related_name='inscripciones')
    clase = models.ForeignKey(Clase, on_delete=models.PROTECT, related_name='inscripciones')
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)

    class Meta:
        unique_together = ('alumno', 'clase')

    def __str__(self):
        return f'{self.alumno} - {self.clase} ({self.estado})'


class Pago(models.Model):
    MEDIO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    ]

    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.PROTECT, related_name='pagos')
    fecha = models.DateField(auto_now_add=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    medio = models.CharField(max_length=20, choices=MEDIO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f'Pago {self.importe} - {self.inscripcion}'
