// mapa.js
function obtenerUbicacionUsuario() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(mostrarUbicacion);
    } else {
        alert("La geolocalización no es compatible con este navegador.");
    }
}

function mostrarUbicacion(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    // Aquí puedes enviar esta información al backend o usarla directamente en el mapa
    // Por ejemplo, podrías almacenar la latitud y longitud en variables globales o en un objeto
    window.ubicacionUsuario = { latitud: lat, longitud: lon }; // Guardar la ubicación del usuario
}
