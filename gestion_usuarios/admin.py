from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'apellido', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'nombre', 'apellido')
    list_filter = ('is_active', 'is_staff')

