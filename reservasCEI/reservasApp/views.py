from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse("Indice de la pagina. Esto es lo primero que los usuarios ven.")

def adminPendientes(request):
	return render(request, 'reservasApp/adminPendientes.html')

def listaArticulos(request):
	return render(request, 'reservasApp/listaArticulos.html')

def listArtAvan(request):
    return render(request, 'reservasApp/busquedaAvanzada.html')

def fichaArticulo(request):
	return render(request, 'reservasApp/fichaArticulo.html')

'''definir'''
def buscar(request):
	return "hola"


