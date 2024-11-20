from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()  # Solo fecha
    hora = models.CharField(
        max_length=8,
        validators=[RegexValidator(regex=r'^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$', message="Formato de hora inválido. Usa hh:mm AM/PM.")]
    )  # Hora en formato 12 horas
    ubicacion = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^-?\d{1,2}\.\d+,\s*-?\d{1,3}\.\d+$', message="Formato de coordenada inválido. Usa 'latitud, longitud'.")]
    )  # Coordenadas
    max_participantes = models.IntegerField()
    participantes = models.ManyToManyField(User, related_name='eventos', blank=True)
    lider = models.ForeignKey(User, related_name='eventos_liderados', on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre


    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    es_lider = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username
