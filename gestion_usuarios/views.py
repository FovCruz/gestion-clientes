from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Usuario,SliderImage,Logo,Producto,Categoria,Etiqueta
from .forms import UsuarioForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator


#--------------  

def load_products(request):
    productos = Producto.objects.all()

    # Aplicar filtros según los parámetros recibidos
    filter_name = request.GET.get('filter_name', '').strip()  # Eliminar espacios
    if filter_name:
        productos = productos.filter(nombre__icontains=filter_name)
    
    min_price = request.GET.get('min_price')
    if min_price:
        productos = productos.filter(precio__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        productos = productos.filter(precio__lte=max_price)
    
    categoria = request.GET.get('category')
    if categoria:
        productos = productos.filter(categoria_id=categoria)

    disponible = request.GET.get('disponible')
    if disponible == '1':
        productos = productos.filter(existencia=True)

    # Ordenar productos
    sort_by = request.GET.get('sort_by', 'asc')
    if sort_by == 'desc':
        productos = productos.order_by('-precio')
    else:
        productos = productos.order_by('precio')

    # Paginación
    paginator = Paginator(productos, 4)  # 6 productos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Retornar el template que muestra solo los productos filtrados
    return render(request, 'productos_filtros.html', {'productos': productos})


def search_products(request):
    query = request.GET.get('query')
    if query:
        products = Producto.objects.filter(nombre__icontains=query)
        results = [{'id': product.id, 'nombre': product.nombre} for product in products]
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse([], safe=False)


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'detalle_producto.html', {'producto': producto})

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
    return render(request, 'resultados_busqueda.html', context)


class ProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'productos.html'
    success_url = reverse_lazy('productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Asegurarse de pasar las categorías
        context['productos'] = Producto.objects.all()  # Asegurarse de pasar los productos también
        return context


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
