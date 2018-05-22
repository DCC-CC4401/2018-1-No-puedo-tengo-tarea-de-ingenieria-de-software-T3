from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import utc

from datetime import *

from reservasApp.forms import NewPersonForm, LoginForm
from .models import *

def index(request):
    return HttpResponse("Indice de la pagina. Esto es lo primero que los usuarios ven.")


def espacios(request, espacio_id=1, dia_actual=datetime.utcnow().replace(tzinfo=utc)):
    horario_espacio = []
    lunes = dia_actual - timedelta(days=dia_actual.weekday())
    lunes_str = lunes.strftime("%d/%m")
    viernes_str = (lunes + timedelta(days=4)).strftime("%d/%m")
    semana = "Semana del " + lunes_str + " al " + viernes_str + " del " + str(dia_actual.year)
    if (not (Espacio.objects.count())):
        generarHorario(espacio_id, lunes, horario_espacio)
        context = {'horario': horario_espacio, 'semana': semana}
        return render(request, 'reservasApp/adminPendientes.html', context)
    else:
        espacios_total = Espacio.objects.all()
        if (request.POST):
            espacio_id = int(request.POST['espacio_selec'])
        espacio = Espacio.objects.get(id=espacio_id)
        generarHorario(espacio_id, lunes, horario_espacio)
        context = {'espacio': espacio, 'espacios_total': espacios_total,
                   'horario': horario_espacio, 'semana': semana, }
        return render(request, 'reservasApp/adminPendientes.html', context)


def generarHorario(espacio_id, dia, horario_espacio, h=9):
    if (not (Espacio.objects.count())):
        for h in (list(range(9, 18))):
            horario = []
            horario.append(str(h) + ":00 - " + str(h + 1) + ":00")  # <td> con la hora
            for d in (list(range(0, 5))):
                horario.append("")
            horario_espacio.append(horario)
    else:
        espacio = Espacio.objects.get(id=espacio_id)
        reservas_espacio = ReservaEspacio.objects.filter(espacio=espacio)
        horario = []
        # lunes a viernes
        dias = [dia,
                dia + timedelta(days=1),
                dia + timedelta(days=2),
                dia + timedelta(days=3),
                dia + timedelta(days=4)]
        horario.append(str(h) + ":00 - " + str(h + 1) + ":00")  # <td> con la hora
        for d in dias:
            a = d.year
            m = d.month
            d2 = d.day
            found = False  # booleano por si encuentra reserva
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
            generarHorario(espacio_id, dia, horario_espacio, h + 1)


def fichaEspacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)
    return render(request, 'reservasApp/fichaEspacio.html', {'espacio': espacio})


def listaArticulos(request):
    return render(request, 'reservasApp/listaArticulos.html')


def busquedaAvanzada(request, articulo_id=1):
    articulos_total = Articulo.objects.all()

    articulo = Articulo.objects.get(id=articulo_id)
    articulo_nombre = Articulo.nombre
    estado = Articulo.estado

    foto_articulo = FotoArticulo.objects.get(id=articulo_id)

    context = {
        'articulo': articulo, 'articulos_total': articulos_total,
        'articulo_nombre': articulo_nombre, 'estado': estado,
        'foto_articulo': foto_articulo
    }

    return render(request, 'reservasApp/busquedaAvanzada.html', context)


def busquedaSimple(request, articulo_id=1):
    articulos_total_simple = Articulo.objects.all()

    articulo_simple = Articulo.objects.get(id=articulo_id)
    articulo_nombre_simple = Articulo.nombre
    estado_simple = Articulo.estado

    foto_articulo_simple = FotoArticulo.objects.get(id=articulo_id)

    context = {
        'articulo_simple': articulo_simple, 'articulos_total_simple': articulos_total_simple,
        'articulo_nombre_simple': articulo_nombre_simple, 'estado_simple': estado_simple,
        'foto_articulo_simple': foto_articulo_simple
    }

    return render(request, 'reservasApp/busquedaSimple.html', context)

def crearUsuario(request):
    if request.method == 'POST':
        form = NewPersonForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('reservasApp:listaArt')
    else:
        form = NewPersonForm()
    return render(request, 'reservasApp/crearUsuario.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('reservasApp:listaArt')
    else:
        form = LoginForm()
    return render(request, 'reservasApp/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('reservasApp:listaArt')

'''definir'''


def buscar(request):
    return "hola"


def reservas(request):
    return render(request, 'reservasApp/reservas.html')
