from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import utc
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from datetime import *

from .forms import NewPersonForm, LoginForm
from .models import *

def index(request):
    return HttpResponse("Indice de la pagina. Esto es lo primero que los usuarios ven.")

@login_required
def listaEspacios(request, espacio_id=1, dia_actual=datetime.utcnow().replace(tzinfo=utc)):
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

@login_required
def fichaEspacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)
    return render(request, 'reservasApp/fichaEspacio.html', {'espacio': espacio})

@login_required
def listaArticulos(request, articulo_id=1):
    articulos = Articulo.objects.all()

    context = {
        'articulos': articulos,
    }

    return render(request, 'reservasApp/listaArticulos.html', context)


# Falta mejorar la busqueda para ignorar mayusculas
@login_required
def busquedaSimple(request):
    if (request.method == 'POST'):
        articulo = request.POST['articulo']
        inventario = Articulo.objects.filter(nombre__iexact=articulo)

        return render(request, 'reservasApp/listaArticulos.html',
                      {'articulos': inventario})  # redirecciona a localhost:8000

    else:
        articulos = Articulo.objects.all()
        return render(request, 'reservasApp/busquedaSimple.html', {'articulos': articulos})

@login_required
def busquedaAvanzada(request):
    if (request.method == 'POST'):
        articulo = request.POST['articulo']
        tipo = request.POST['tipo']
        estado = request.POST['estado']

        # campos estado y tipo existen
        if (estado != "4" and tipo != "0"):
            if (articulo != ""):  # campo articulo existe
                inventario = Articulo.objects.filter(nombre__iexact=articulo, estado=estado, tipo=tipo)
            else:  # campo articulo no existe
                inventario = Articulo.objects.filter(estado=estado, tipo=tipo)

        # campo estado existe pero no tipo
        elif (estado != "4"):
            if (articulo != ""):
                inventario = Articulo.objects.filter(nombre__iexact=articulo, estado=estado)
            else:
                inventario = Articulo.objects.filter(estado=estado)

        # campo tipo existe pero no estado
        elif (tipo != "0"):
            if (articulo != ""):  # campo articulo existe
                inventario = Articulo.objects.filter(nombre__iexact=articulo, tipo=tipo)
            else:  # campo articulo no existe
                inventario = Articulo.objects.filter(tipo=tipo)

        # campo articulo pero no tipo ni estado
        elif (articulo != ""):
            inventario = Articulo.objects.filter(nombre__iexact=articulo)

        # Ningun campo existe
        else:
            inventario = Articulo.objects.all()

        return render(request, 'reservasApp/listaArticulos.html', {'articulos': inventario})

    else:
        articulos = Articulo.objects.all()
        print("hola")
        return render(request, 'reservasApp/busquedaAvanzada.html', {'articulos': articulos})


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
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('reservasApp:listaArt')
    else:
        form = LoginForm()
    return render(request, 'reservasApp/login.html', {'form': form})

@login_required
def logoutView(request):
    logout(request)
    return redirect('reservasApp:listaArt')



@login_required
def fichaArticulo(request):
    articulo_id = request.GET['idart']
    art = get_object_or_404(Articulo, id=articulo_id)
    nombre = art.nombre
    estado = art.estado
    descripcion = art.descripcion
    # reservas = ReservaArticulo.objects.filter(articulo=art)
    # context = {'nombre': nombre, 'estado': estado, 'descripcion': descripcion, 'idarticulo': articulo_id, 'reservas': reservas}
    context = {'nombre': nombre, 'estado': estado, 'descripcion': descripcion, 'idarticulo': articulo_id}
    return render(request, 'reservasApp/fichaArticulo.html', context)


@login_required
def exito(request):
    if request.method == 'POST':
        idarticulo = request.POST['id_articulo']
        fecha_i = request.POST['fecha_i']
        fecha_f = request.POST['fecha_f']
        hora_i = request.POST['hora_i']
        hora_f = request.POST['hora_f']
        art = get_object_or_404(Articulo, id=idarticulo)
        art.estado = 2
        art.save()
        nuevo = ReservaArticulo(articulo=art, fecha_inicial=fecha_i, fecha_final=fecha_f, hora_inicial=hora_i,
                            hora_final=hora_f, estado=2)
        nuevo.save()
    return render(request, 'reservasApp/exito.html')


@login_required
def perfil(request):
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    if (request.user.is_authenticated):
        if (request.user.groups.filter(name='Administrador').exists()):
            reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
            context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
            return render(request, 'reservasApp/perfiladmin.html', context)
        else:
            reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)[:10]
            context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
            return render(request, 'reservasApp/perfil.html', context)

@login_required
def eliminar_pendientesesp(request):
    for i in request.POST.getlist("reserva"):
        ReservaEspacio.objects.filter(id=i).delete()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfil.html', context)

@login_required
def eliminar_pendientesart(request):
    for i in request.POST.getlist("reserva"):
        ReservaArticulo.objects.filter(id=i).delete()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfil.html', context)

@login_required
def aprobarart(request):
    for i in request.POST.getlist("reserva"):
        r = ReservaArticulo.objects.get(id=i)
        r.estado = 1
        r.save()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfiladmin.html', context)

@login_required
def rechazarart(request):
    for i in request.POST.getlist("reserva"):
        r = ReservaArticulo.objects.get(id=i)
        r.estado = 0
        r.save()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfiladmin.html', context)

@login_required
def aprobaresp(request):
    for i in request.POST.getlist("reserva"):
        r = ReservaEspacio.objects.get(id=i)
        r.estado = 1
        r.save()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfiladmin.html', context)

@login_required
def rechazaresp(request):
    for i in request.POST.getlist("reserva"):
        r = ReservaEspacio.objects.get(id=i)
        r.estado = 0
        r.save()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfiladmin.html', context)


def buscar(request):
    return "hola"
