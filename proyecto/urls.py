from django.contrib import admin
from django.urls import path, include
from gestion_usuarios.views import HomeView, CustomLoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_usuarios.urls')),  # Esto incluye las URLs de la aplicación 'gestion_usuarios'
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
] 