from django.contrib import admin
from .models import Usuario,SliderImage

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'apellido', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'nombre', 'apellido')
    list_filter = ('is_active', 'is_staff')


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image', 'h2_text', 'h4_text', 'button_text')
    fields = ('image', 'caption', 'h2_text', 'h4_text', 'paragraph', 'button_text', 'button_url')
