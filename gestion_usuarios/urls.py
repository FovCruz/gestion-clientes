from django.urls import path
from .views import (
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
    HomeView,UserDashView
)

urlpatterns = [
    path('dashboard/', UserDashView.as_view(), name='dashboard'),
    path('gestion-usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('', HomeView.as_view(), name='home'),
]
