from django import forms
from .models import Evento
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class EventoForm(forms.ModelForm):
    ubicacion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Coordenadas del lugar del evento'}),
    )
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del evento'}),
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Descripción del evento'}),
    )
    max_participantes = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Número máximo de participantes'}),
    )
    lider = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'placeholder': 'Líder del evento'}),
    )
    fecha = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/AAAA'}),
        input_formats=['%d/%m/%Y']
    )
    hora = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'hh:mm AM/PM'}),
        validators=[RegexValidator(regex=r'^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$', message="Formato de hora inválido. Usa hh:mm AM/PM.")]
    )
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'hora', 'ubicacion', 'max_participantes', 'lider']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
