from django.contrib import admin

from .models import Alumno, Profesor


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'usuario')
    search_fields = ('nombre', 'apellido', 'dni')


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'activo')
    search_fields = ('nombre', 'apellido', 'dni')
