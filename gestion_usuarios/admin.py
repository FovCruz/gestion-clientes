from django.contrib import admin
from .models import Usuario,SliderImage,Logo,Producto,Categoria, Etiqueta

#=======================================================

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'precioOferta', 'existencia']
    list_filter = ['categoria', 'etiquetas']
    search_fields = ['nombre', 'descripcionCorta', 'descripcionLarga', 'codigoProducto']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ['nombre']


#carga de modelo con sus atributos a mostrar en el panel
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'apellido', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'nombre', 'apellido')
    list_filter = ('is_active', 'is_staff')

#carga de modelo con sus atributos a mostrar en el panel

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image', 'image_mobile', 'h2_text', 'h4_text', 'button_text')
    fields = ('image', 'image_mobile', 'caption', 'h2_text', 'h4_text', 'paragraph', 'button_text', 'button_url')


#carga de modelo con sus atributos a mostrar en el panel
class LogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagen')
    search_fields = ('id',)

admin.site.register(Logo, LogoAdmin)
