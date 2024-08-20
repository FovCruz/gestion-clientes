from django.urls import path
from .views import (
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
)

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario_list'),
    path('crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]
