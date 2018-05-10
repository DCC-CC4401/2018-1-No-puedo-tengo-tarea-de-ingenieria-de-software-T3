from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    return HttpResponse("Indice de la pagina. Esto es lo primero que los usuarios ven.")


def espacios(request, espacio_id=1):
    espacio = Espacio.objects.get(id=espacio_id)
    espacios_total = Espacio.objects.all()
    context = {'espacio': espacio, 'espacios_total': espacios_total}
    return render(request, 'reservasApp/adminPendientes.html', context)


def cambiarespacio(request):
    espacio_selecc = Espacio.objects.get(id=request.POST['espacio_selec'])
    espacios_total = Espacio.objects.all()
    context = {'espacio': espacio_selecc, 'espacios_total': espacios_total}
    return render(request, 'reservasApp/adminPendientes.html', context)


def fichaEspacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)
    return render(request, 'reservasApp/fichaEspacio.html', {'espacio': espacio})


def listaArticulos(request):
    return render(request, 'reservasApp/listaArticulos.html')


def busquedaAvanzada(request):
    return render(request, 'reservasApp/busquedaAvanzada.html')


'''definir'''


def buscar(request):
    return "hola"
