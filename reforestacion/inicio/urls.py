# inicio/urls.py
from django.urls import path
from .views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),  # Asegúrate de que el patrón aquí sea correcto
]

#aquí se importa la vista inicio desde el módulo views de la aplicación inicio. Luego, se define una lista urlpatterns que contiene una única ruta que apunta a la vista inicio. La ruta es una cadena vacía, lo que significa que la vista inicio se ejecutará cuando se acceda a la URL base del sitio. El nombre de la ruta es inicio.