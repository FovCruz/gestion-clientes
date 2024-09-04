from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve
from .views import HomeView, ProductosView,UserDashView, UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, CustomLoginView,buscar_productos,detalle_producto


urlpatterns = [
    #path('', banner_view, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', UserDashView.as_view(), name='dashboard'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('productos/', ProductosView.as_view(), name='productos'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
    path('buscar/', buscar_productos, name='buscar_productos'),
    ]


if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)