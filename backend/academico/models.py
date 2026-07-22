from django.db import models

from personas.models import Profesor
from usuarios.models import Institucion


class Curso(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, related_name='cursos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    duracion = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Clase(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='clases')
    cupo = models.PositiveIntegerField()
    aula = models.CharField(max_length=50, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    profesores = models.ManyToManyField(
        Profesor, through='ClaseProfesor', related_name='clases',
    )

    def __str__(self):
        return f'{self.curso.nombre} - {self.aula} ({self.fecha_inicio})'


class ClaseProfesor(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profesor', 'clase')

    def __str__(self):
        return f'{self.profesor} - {self.clase}'


class Horario(models.Model):
    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f'{self.clase} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}'


class Precio(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='precios')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.curso.nombre} - {self.monto} desde {self.fecha_desde}'
