# eventos/urls.py
from django.urls import path
from .views import lista_eventos, mapa_eventos, crear_evento, detalle_evento, editar_evento, eliminar_evento, registrarse_evento, cancelar_registro_evento, grafo_dijkstra

urlpatterns = [
    path('', lista_eventos, name='eventos'),  # Asegúrate de que aquí está el nombre correcto
    path('mapa/', mapa_eventos, name='mapa_eventos'),
    path('crear-evento/', crear_evento, name='crear_evento'),
    path('editar/<int:id>/', editar_evento, name='editar_evento'),  # Ruta para editar el evento
    path('eliminar/<int:id>/', eliminar_evento, name='eliminar_evento'),# Ruta para eliminar el evento
    path('<int:id>/', detalle_evento, name='detalle_evento'),  # Detalle del evento
    path('eventos/<int:id>/registrarse/', registrarse_evento, name='registrarse_evento'),
    path('eventos/<int:evento_id>/cancelar/', cancelar_registro_evento, name='cancelar_registro_evento'),
    path('dijkstra/', grafo_dijkstra, name='grafo_dijkstra'),
]


