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


class Alumno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='alumno')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'


class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profesor')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'


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


class Precio(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='precios')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.curso.nombre} - {self.monto} desde {self.fecha_desde}'


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
