from django.db import transaction
from rest_framework import serializers

from academico.models import Clase, Curso
from inscripciones.models import Inscripcion, Pago
from personas.models import Alumno
from usuarios.models import Usuario


class RegistroAlumnoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    dni = serializers.CharField(max_length=20)
    telefono = serializers.CharField(max_length=30, required=False, allow_blank=True)
    direccion = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Ya existe una cuenta con ese email.')
        return value

    def validate_dni(self, value):
        if Alumno.objects.filter(dni=value).exists():
            raise serializers.ValidationError('Ya existe un alumno con ese DNI.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            rol=Usuario.ROL_ALUMNO,
        )
        return Alumno.objects.create(
            usuario=usuario,
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            dni=validated_data['dni'],
            telefono=validated_data.get('telefono', ''),
            direccion=validated_data.get('direccion', ''),
        )


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'descripcion', 'duracion', 'activo']


class ClaseSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    vacantes = serializers.SerializerMethodField()

    class Meta:
        model = Clase
        fields = [
            'id', 'curso', 'cupo', 'aula', 'fecha_inicio', 'fecha_fin',
            'activo', 'vacantes',
        ]

    def get_vacantes(self, obj):
        ocupadas = obj.inscripciones.filter(
            estado__in=[Inscripcion.ESTADO_PENDIENTE, Inscripcion.ESTADO_CONFIRMADA],
        ).count()
        return obj.cupo - ocupadas


class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = ['id', 'alumno', 'clase', 'fecha', 'estado']
        read_only_fields = ['alumno', 'fecha', 'estado']

    def validate_clase(self, clase):
        ocupadas = clase.inscripciones.filter(
            estado__in=[Inscripcion.ESTADO_PENDIENTE, Inscripcion.ESTADO_CONFIRMADA],
        ).count()
        if ocupadas >= clase.cupo:
            raise serializers.ValidationError('No hay vacantes disponibles en esta clase.')
        return clase


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'inscripcion', 'fecha', 'importe', 'medio', 'estado']
