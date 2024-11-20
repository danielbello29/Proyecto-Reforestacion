from django.shortcuts import render

def inicio(request):
    es_lider = request.user.groups.filter(name="Líderes").exists() if request.user.is_authenticated else False
    return render(request, 'inicio/inicio.html', {'es_lider': es_lider})

#aquí se define la vista de inicio, que se encarga de renderizar la plantilla inicio.html. Además, se pasa un contexto con la variable es_lider, que indica si el usuario autenticado es un líder o no. Para ello, se verifica si el usuario pertenece al grupo "Líderes". Si el usuario no está autenticado, se asigna False a es_lider.