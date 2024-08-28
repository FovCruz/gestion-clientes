from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from datetime import timedelta

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    h2_text = models.CharField(max_length=255, blank=True, null=True)
    h4_text = models.CharField(max_length=255, blank=True, null=True)
    paragraph = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.caption or 'Slider Image'


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
