from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
import os


# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='productos/')
    descripcionCorta = models.CharField(max_length=255, default='Descripción corta no disponible')
    descripcionLarga = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precioOferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    existencia = models.BooleanField(default=True)
    codigoProducto = models.CharField(max_length=100, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    etiquetas = models.ManyToManyField('Etiqueta', blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Etiqueta/Tag
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


#CARRUSEL DE LOGOS 
class Logo(models.Model):
    imagen = models.ImageField(upload_to='logos/')
    
    def __str__(self):
        return f"Logo {self.id}"
    
    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Carrusel de logos"

#BANNER SLIDER DEL HOME
class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/', verbose_name='Imagen versión escritorio')
    image_mobile = models.ImageField(upload_to='slider_images/mobile/', blank=True, null=True, verbose_name='Imagen versión móvil')  # Nuevo campo
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name='Título')
    h2_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Texto H2')
    h4_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Texto H4')
    paragraph = models.TextField(blank=True, null=True, verbose_name='Párrafo')
    button_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='Texto del Botón')
    button_url = models.URLField(blank=True, null=True, verbose_name='URL del Botón')

    def clean(self):
        if not self.image:
            raise ValidationError('Debe haber al menos una imagen para mostrar en el banner.')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.image_mobile:
            if os.path.isfile(self.image_mobile.path):
                os.remove(self.image_mobile.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Imagen de Slider'
        verbose_name_plural = 'Imágenes de Slider'

    def __str__(self):
        return self.caption or 'Slider Image'



#formulario para la creacion de usuarios
class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    plataforma = models.CharField(max_length=50, choices=[
        ('Duplex Play', 'Duplex Play'),
        ('IPTV Smarters', 'IPTV Smarters'),
        ('Smart IPTV', 'Smart IPTV'),
        # Agrega más opciones aquí
    ])
    fecha_expiracion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    habilitado = models.BooleanField(default=True)
    nombre_usuario_plataforma = models.CharField(max_length=50, blank=True)
    clave_usuario_plataforma = models.CharField(max_length=50, blank=True)
    # Modificación para evitar conflictos de nombres
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def agregar_meses(self, meses):
        if not self.fecha_expiracion:
            self.fecha_expiracion = timezone.now().date()
        self.fecha_expiracion += timedelta(days=meses * 30)
        self.save()
