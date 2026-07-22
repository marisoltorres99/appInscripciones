from django.contrib import admin

from .models import Clase, ClaseProfesor, Curso, Horario, Precio


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


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('curso', 'monto', 'fecha_desde', 'fecha_hasta')
