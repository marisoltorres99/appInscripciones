from django.contrib import admin

from .models import Inscripcion, Pago


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'clase', 'fecha', 'estado')
    list_filter = ('estado',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'importe', 'medio', 'estado', 'fecha')
    list_filter = ('estado', 'medio')
