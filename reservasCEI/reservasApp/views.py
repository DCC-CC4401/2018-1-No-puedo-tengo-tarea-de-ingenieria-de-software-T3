from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
from datetime import *
from django.utils.timezone import utc
from django.shortcuts import redirect

def index(request):
    return HttpResponse("Indice de la pagina. Esto es lo primero que los usuarios ven.")


def espacios(request, espacio_id=1, dia_actual=datetime.utcnow().replace(tzinfo=utc)):
    horario_espacio = []
    lunes = dia_actual - timedelta(days = dia_actual.weekday())
    lunes_str = lunes.strftime("%d/%m")
    viernes_str = (lunes + timedelta(days = 4)).strftime("%d/%m")
    semana = "Semana del " + lunes_str + " al " + viernes_str + " del " + str(dia_actual.year)
    if (not(Espacio.objects.count())):
        generarHorario(espacio_id, lunes, horario_espacio)
        context = {'horario': horario_espacio, 'semana': semana}
        return render(request, 'reservasApp/adminPendientes.html',context)
    else:
        espacios_total = Espacio.objects.all()
        if (request.POST):
            espacio_id = int(request.POST['espacio_selec'])
        espacio = Espacio.objects.get(id=espacio_id)
        generarHorario(espacio_id, lunes, horario_espacio)
        context = {'espacio': espacio, 'espacios_total': espacios_total,
                   'horario': horario_espacio, 'semana': semana,}
        return render(request, 'reservasApp/adminPendientes.html', context)

def generarHorario(espacio_id, dia, horario_espacio, h=9):
    if (not(Espacio.objects.count())):
        for h in (list(range(9,18))):
            horario = []
            horario.append(str(h)+":00 - " + str(h+1)+":00") #<td> con la hora
            for d in (list(range(0,5))):
                horario.append("")
            horario_espacio.append(horario)
    else:
        espacio = Espacio.objects.get(id=espacio_id)
        reservas_espacio = ReservaEspacio.objects.filter(espacio=espacio)
        horario = []
        #lunes a viernes
        dias = [dia,
                dia + timedelta(days = 1),
                dia + timedelta(days = 2),
                dia + timedelta(days = 3),
                dia + timedelta(days = 4)]
        horario.append(str(h)+":00 - " + str(h+1)+":00") #<td> con la hora
        for d in dias:
            a = d.year
            m = d.month
            d2 = d.day
            found = False #booleano por si encuentra reserva
            for r in reservas_espacio:
                if (r.fecha_inicial.day == d2 and
                    r.fecha_inicial.month == m and
                    r.fecha_inicial.year == a and
                    (r.fecha_inicial.hour <= h and r.fecha_final.hour > h)):
                    horario.append(r.espacio)
                    found = True
                    break;
            if not found:
                horario.append("")
        horario_espacio.append(horario)
        if (h < 17):
            generarHorario(espacio_id, dia, horario_espacio,h+1)

def listaArticulos(request):
    return render(request, 'reservasApp/listaArticulos.html')


def busquedaAvanzada(request):
    return render(request, 'reservasApp/busquedaAvanzada.html')

def busquedaSimple(request):
    return render(request, 'reservasApp/busquedaSimple.html')


'''definir'''


def buscar(request):
    return "hola"

def reservas(request):
    return render(request, 'reservasApp/reservas.html')
