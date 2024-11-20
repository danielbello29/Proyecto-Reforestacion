from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
import requests
import folium
from geopy.distance import great_circle
from django.utils import timezone
import heapq
from django.template.loader import get_template
import os

# Vista para mostrar la lista de eventos
def lista_eventos(request):
    eventos = Evento.objects.all()
    
    # Verificar si el usuario es líder
    es_lider = request.user.groups.filter(name="Líderes").exists() if request.user.is_authenticated else False
    
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos,
        'es_lider': es_lider
    }) 

# Vista para crear un nuevo evento
@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.lider = request.user  # Asigna el líder como el usuario actual
            evento.save()
            return redirect('eventos')  # Redirige a la lista de eventos
    else:
        form = EventoForm()

    return render(request, 'eventos/crear_evento.html', {'form': form})

# Vista para editar un evento existente
@login_required
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('detalle_evento', id=evento.id)
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

# Vista para eliminar un evento
@login_required
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        evento.delete()
        return redirect('eventos')  # Redirigir a la lista de eventos después de eliminar

    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

# Vista para mostrar los detalles de un evento
@login_required
def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    es_lider = request.user.groups.filter(name="Líderes").exists()  # Verificar si el usuario es líder
    participantes = evento.participantes.all()  # Obtener los participantes registrados

    # Manejo de registro/cancelación al evento
    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'registrarse':
            if request.user not in participantes and len(participantes) < evento.max_participantes:
                evento.participantes.add(request.user)
                evento.save()
        elif accion == 'cancelar':
            if request.user in participantes:
                evento.participantes.remove(request.user)
                evento.save()

        return redirect('detalle_evento', id=evento.id)

    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
        'es_lider': es_lider,
        'participantes': participantes,
        'es_participante': request.user in participantes  # Si el usuario ya está registrado
    })

@login_required
def registrarse_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    # Agregar al usuario como participante si no está ya registrado
    if request.user not in evento.participantes.all():
        evento.participantes.add(request.user)
    
    return redirect('detalle_evento', id=evento.id)

@login_required
def cancelar_registro_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    # Remover al usuario del evento
    evento.participantes.remove(request.user)  # Asegúrate de que 'participantes' es una relación correcta
    return redirect('detalle_evento', id=evento.id)  # Redirigir al detalle del evento
    
def obtener_ubicacion_por_ip(request):	
    api_key = '6726cde3224d452db06f75d32733a882'  # Reemplaza con tu API Key de OpenCage
    url = f'https://api.opencagedata.com/geocode/v1/json?q={request.META["ip"]}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if data and data['results']:
        return data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']
    else:
        return None, None



def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}  # Inicializar distancias
    distancias[inicio] = 0  # La distancia desde el nodo de inicio a sí mismo es 0
    caminos = {nodo: [] for nodo in grafo}  # Rutas más cortas

    # Nodos visitados
    visitados = set()

    while visitados != set(grafo.keys()):
        # Seleccionar el nodo no visitado con la distancia más corta
        nodo_actual = min((nodo for nodo in grafo if nodo not in visitados), key=lambda nodo: distancias[nodo])

        visitados.add(nodo_actual)

        for vecino in grafo[nodo_actual]['vecinos']:
            if vecino in visitados:
                continue
            nueva_distancia = distancias[nodo_actual] + grafo[nodo_actual]['distancias'][vecino]
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                caminos[vecino] = caminos[nodo_actual] + [nodo_actual]

    return distancias, caminos

# Función para calcular la distancia entre dos puntos
def calcular_distancia(coord1, coord2):
    return great_circle(coord1, coord2).kilometers

# Función para calcular el puntaje de un evento
def calcular_puntaje(evento, distancias, grafo):
    cantidad_personas = grafo.get(evento, {}).get('cantidad_personas', 0)
    dias_restantes = grafo.get(evento, {}).get('dias_restantes', 0)
    distancia = distancias.get(evento, float('inf'))  # Valor por defecto muy alto si no se encuentra

    # Asegurarse de que todos los valores son números
    if cantidad_personas is None:
        cantidad_personas = 0  # Valor por defecto
    if dias_restantes is None:
        dias_restantes = 0  # Valor por defecto
    if distancia is None:
        distancia = float('inf')  # Valor por defecto muy alto si no se encuentra

    # Ajustar el puntaje para priorizar menos participantes
    puntaje = distancia + (cantidad_personas * 1.5) + (dias_restantes * 0.3)

    return puntaje 


# Vista para el mapa
def mapa_eventos(request):
    user_lat = request.GET.get('lat', None)
    user_lng = request.GET.get('lng', None)

    # Si se recibe latitud y longitud, se usa; de lo contrario, se asigna una predeterminada
    if user_lat and user_lng:
        user_location = (float(user_lat), float(user_lng))
    else:
        user_location = (20.673593, -103.392853)  # Coordenadas predeterminadas si no se obtiene la ubicación

    eventos = Evento.objects.all()
    grafo = {'user_location': {'coord': user_location, 'vecinos': [], 'distancias': {}}}
    event_nodes = []

    for evento in eventos:
        lat, lng = map(float, evento.ubicacion.split(','))
        event_nodes.append(evento.nombre)
        
        # Convertir evento.fecha a datetime.date para evitar errores
        fecha_evento = evento.fecha if isinstance(evento.fecha, timezone.datetime) else evento.fecha
        dias_restantes = (fecha_evento - timezone.now().date()).days if evento.fecha else None

        grafo[evento.nombre] = {
            'coord': (lat, lng),
            'vecinos': ['user_location'],
            'distancias': {'user_location': calcular_distancia(user_location, (lat, lng))},
            'cantidad_personas': evento.participantes.count(),
            'dias_restantes': dias_restantes
        }
        grafo['user_location']['vecinos'].append(evento.nombre)
        grafo['user_location']['distancias'][evento.nombre] = calcular_distancia(user_location, (lat, lng))

    if len(grafo) < 2:
        return render(request, 'mapa.html', {'error': 'No hay eventos disponibles para calcular rutas.'})

    # Calcular las distancias usando Dijkstra
    distancias, caminos = dijkstra(grafo, 'user_location')

    # Calcular el evento óptimo
    evento_mejor_opcion_nombre = min(event_nodes, key=lambda nodo: calcular_puntaje(nodo, distancias, grafo))
    evento_mejor_opcion = eventos.get(nombre=evento_mejor_opcion_nombre)

    # Crear el mapa
    m = folium.Map(location=user_location, zoom_start=15)

    # Añadir marcador para el usuario
    folium.Marker(user_location, popup='Tu ubicación', icon=folium.Icon(color='green')).add_to(m)

    # Añadir marcadores para los eventos
    for node in event_nodes:
        lat, lng = grafo[node]['coord']
        cantidad_participantes = grafo[node]['cantidad_personas']
        max_participantes = eventos.get(nombre=node).max_participantes
        fecha_evento = eventos.get(nombre=node).fecha.strftime('%d/%m/%Y') if eventos.get(nombre=node).fecha else "Fecha no disponible"

        folium.Marker(
            [lat, lng],
            popup=f"{node}\n{cantidad_participantes}/{max_participantes}\n{fecha_evento}",
            icon=folium.Icon(color='red')
        ).add_to(m)

    camino = caminos[evento_mejor_opcion_nombre] + [evento_mejor_opcion_nombre]
    for i in range(len(camino) - 1):
        start = grafo[camino[i]]['coord']
        end = grafo[camino[i + 1]]['coord']
        folium.PolyLine(locations=[start, end], color='green', weight=5).add_to(m)

    mapa_html = m._repr_html_()

    return render(request, 'mapa.html', {
        'mapa': mapa_html,
        'eventos': eventos,
        'evento_recomendado_id': evento_mejor_opcion.id,
        'evento_recomendado_titulo': evento_mejor_opcion.nombre
    })


def grafo_dijkstra(request):
    eventos = Evento.objects.all()
    user_location = (20.673593, -103.392853)  # Coordenadas predeterminadas del usuario
    grafo = {'user_location': {'coord': user_location, 'vecinos': [], 'distancias': {}}}

    for evento in eventos:
        lat, lng = map(float, evento.ubicacion.split(','))
        grafo[evento.nombre] = {
            'coord': (lat, lng),
            'vecinos': ['user_location'],
            'distancias': {'user_location': calcular_distancia(user_location, (lat, lng))},
            'cantidad_personas': evento.max_participantes,
            'dias_restantes': (evento.fecha - timezone.now()).days,
        }
        grafo['user_location']['vecinos'].append(evento.nombre)
        grafo['user_location']['distancias'][evento.nombre] = calcular_distancia(user_location, (lat, lng))

    # Calcular distancias usando Dijkstra
    distancias, caminos = dijkstra(grafo, 'user_location')

    # Calcular puntajes para cada evento
    puntajes = {evento: calcular_puntaje(evento, distancias, grafo) for evento in grafo if evento != 'user_location'}

    return render(request, 'eventos/grafo_dijkstra.html', {
        'distancias': distancias,
        'caminos': caminos,
        'grafo': grafo,
        'puntajes': puntajes,  # Pasar puntajes a la plantilla
    })
