from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Alumno,
    Clase,
    ClaseProfesor,
    Curso,
    Horario,
    Inscripcion,
    Institucion,
    Pago,
    Precio,
    Profesor,
    Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos de la aplicación', {'fields': ('rol', 'institucion')}),
    )
    list_display = ('username', 'email', 'rol', 'institucion', 'is_active')


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'activo')


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'usuario')
    search_fields = ('nombre', 'apellido', 'dni')


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'activo')
    search_fields = ('nombre', 'apellido', 'dni')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucion', 'activo')


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1


class ClaseProfesorInline(admin.TabularInline):
    model = ClaseProfesor
    extra = 1


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('curso', 'aula', 'cupo', 'fecha_inicio', 'activo')
    inlines = [HorarioInline, ClaseProfesorInline]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'clase', 'fecha', 'estado')
    list_filter = ('estado',)


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('curso', 'monto', 'fecha_desde', 'fecha_hasta')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'importe', 'medio', 'estado', 'fecha')
    list_filter = ('estado', 'medio')
