from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Usuario,SliderImage,Logo,Producto
from .forms import UsuarioForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#--------------  
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(descripcionCorta__icontains=query) | 
            Q(descripcionLarga__icontains=query) | 
            Q(categoria__nombre__icontains=query) |
            Q(etiquetas__nombre__icontains=query)
        ).distinct()

    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'tu_template.html', context)


class ProductosView(LoginRequiredMixin,TemplateView):
    template_name = 'productos.html'
    success_url = reverse_lazy('productos')

class UserDashView(LoginRequiredMixin,TemplateView):
    template_name = 'usuarios/dashboard.html'
    success_url = reverse_lazy('dashboard')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_images'] = SliderImage.objects.all()
        context['logo_images'] = Logo.objects.all()
        context['productos'] = Producto.objects.all()  # Agrega productos al contexto
        return context

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        for usuario in queryset:
            if usuario.fecha_expiracion:
                usuario.dias_restantes = (usuario.fecha_expiracion - timezone.now().date()).days
            else:
                usuario.dias_restantes = None  # Maneja el caso donde no hay fecha de expiración
        return queryset

    success_url = reverse_lazy('usuario_list')


class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

@method_decorator(csrf_exempt, name='dispatch')
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuario_list')

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, se maneja de forma especial
            response = self.delete(request, *args, **kwargs)
            return JsonResponse({'success': True})
        else:
            # Si no es una solicitud AJAX, se maneja normalmente
            return super().post(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
