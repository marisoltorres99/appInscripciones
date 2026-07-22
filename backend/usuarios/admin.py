from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Institucion, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos de la aplicación', {'fields': ('rol', 'institucion')}),
    )
    list_display = ('username', 'email', 'rol', 'institucion', 'is_active')


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'activo')
