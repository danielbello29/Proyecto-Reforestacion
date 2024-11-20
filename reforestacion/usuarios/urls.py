# usuarios/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView # Importa la vista de inicio de sesión
from .views import register

urlpatterns = [
    path('register/', register, name='register'),  # Registro
    path('login/', LoginView.as_view(), name='login'),  # Ingreso
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),  # Cierre de sesión
]