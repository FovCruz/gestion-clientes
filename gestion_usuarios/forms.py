# gestion-usuarios/forms.py
from django import forms
from .models import Usuario
from django.utils import timezone
import uuid

class UsuarioForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm',
            'placeholder': 'Seleccione la fecha de inicio',
            'onfocus': "(this.type='date')",
        }),
        initial=timezone.now().date()
    )
    
    meses = forms.ChoiceField(
        choices=[
            (1, '1 mes'), (2, '2 meses'), (3, '3 meses'), (4, '4 meses'), (6, '6 meses'), (12, '12 meses')
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellido',
            'plataforma',
            'fecha_inicio',
            'meses',
            'nombre_usuario_plataforma',
            'clave_usuario_plataforma',
            'observaciones',
            'habilitado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ingrese el nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ingrese el apellido'}),
            'plataforma': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'nombre_usuario_plataforma': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ingrese el nombre de usuario'}),
            'clave_usuario_plataforma': forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ingrese la clave de usuario'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm bg-light', 'placeholder': 'Ingrese observaciones','rows':3}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        meses = self.cleaned_data.get('meses')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        # Calcular la fecha de expiración basada en los meses seleccionados
        fecha_expiracion = fecha_inicio + timezone.timedelta(days=int(meses) * 30)
        instance.fecha_expiracion = fecha_expiracion

        # Asignar un username único si no se proporciona
        if not instance.username:
            instance.username = f"user_{uuid.uuid4().hex[:8]}"

        if commit:
            instance.save()
        return instance
