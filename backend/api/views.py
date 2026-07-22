from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from academico.models import Clase, Curso
from inscripciones.models import Inscripcion, Pago

from .serializers import (
    ClaseSerializer,
    CursoSerializer,
    InscripcionSerializer,
    PagoSerializer,
    RegistroAlumnoSerializer,
)


class RegistroAlumnoView(generics.CreateAPIView):
    serializer_class = RegistroAlumnoSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alumno = serializer.save()
        data = {
            'id': alumno.id,
            'email': alumno.usuario.email,
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'dni': alumno.dni,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Curso.objects.filter(activo=True)
    serializer_class = CursoSerializer
    permission_classes = [permissions.AllowAny]


class ClaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clase.objects.filter(activo=True).select_related('curso')
    serializer_class = ClaseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        curso_id = self.request.query_params.get('curso')
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        return queryset


def _alumno_del_usuario(user):
    alumno = getattr(user, 'alumno', None)
    if alumno is None:
        raise PermissionDenied('Esta acción requiere una cuenta de alumno.')
    return alumno


class InscripcionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = InscripcionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        alumno = _alumno_del_usuario(self.request.user)
        return Inscripcion.objects.filter(alumno=alumno).select_related('clase', 'clase__curso')

    def perform_create(self, serializer):
        alumno = _alumno_del_usuario(self.request.user)
        serializer.save(alumno=alumno)


class PagoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        alumno = _alumno_del_usuario(self.request.user)
        return Pago.objects.filter(inscripcion__alumno=alumno).select_related('inscripcion')
