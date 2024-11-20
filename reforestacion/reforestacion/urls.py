# reforestacion/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', include('inicio.urls')),           # Incluyendo las URLs de inicio
    path('eventos/', include('eventos.urls')),  # URLs para eventos
    path('register/', include('usuarios.urls')), # URLs para usuarios
]
