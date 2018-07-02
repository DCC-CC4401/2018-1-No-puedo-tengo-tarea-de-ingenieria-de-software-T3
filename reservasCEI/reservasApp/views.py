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


def busquedaSimple(request):
	return render(request, 'reservasApp/busquedaSimple.html')


def fichaArticulo(request):
	#art = get_object_or_404(Articulo, id=articulo_id)
	#nombre = art.nombre
	#estado = art.estado
    #descripcion = art.descripcion
    nombre = "Mesa"
    estado = "Disponible"
    descripcion = "Mesa mediana de 3x4 metros"
    context = {'nombre': nombre, 'estado': estado, 'descripcion' : descripcion, 'idarticulo': 123}
    return render(request, 'reservasApp/fichaArticulo.html', context)

def exito(request):
    if request.method == 'POST':
        idarticulo = request.POST['id_articulo']
        fecha_i = request.POST['fecha_i']
        fecha_f = request.POST['fecha_f']
        hora_i = request.POST['hora_i']
        hora_f = request.POST['hora_f']
        nuevo = ReservaArticulo(articulo=idarticulo, fecha_inicial=fecha_i, fecha_final=fecha_f, hora_inicial=hora_i, hora_final=hora_f, estado=2)
        nuevo.save()
    return render(request, 'reservasApp/exito.html')

def perfil(request):
    return render(request, 'reservasApp/perfil.html')

'''definir'''


def buscar(request):
	return "hola"


