from django.contrib import admin
from .models import Evento, PerfilUsuario

# Registra los modelos en el administrador
admin.site.register(Evento)
admin.site.register(PerfilUsuario)
