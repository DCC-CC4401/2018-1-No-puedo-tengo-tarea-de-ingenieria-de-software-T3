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
from django.utils.timezone import utc
from django.contrib.auth.models import Group

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
                        r.estado == 1 and
                        (r.hora_inicial <= h and r.hora_final > h)):
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
    articulos = Articulo.objects.all()

    fotosArt = FotoArticulo.objects.all()

    context = {
        'articulos': articulos,
        'fotosArt': fotosArt
    }

    return render(request, 'reservasApp/listaArticulos.html', context)

def busquedaSimple(request):
    if (request.method == 'POST'):
        articulo = request.POST['articulo']
        inventario = Articulo.objects.filter(nombre__iexact=articulo)

        return render(request, 'reservasApp/listaArticulos.html',
                      {'articulos': inventario})  # redirecciona a localhost:8000

    else:
        articulos = Articulo.objects.all()
        return render(request, 'reservasApp/busquedaSimple.html', {'articulos': articulos})


def busquedaAvanzada(request):
    if (request.method == 'POST'):
        articulo = request.POST['articulo']
        estado = request.POST['estado']
        fecha_i = request.POST['fecha_i']
        fecha_f = request.POST['fecha_f']

        # campo fechas existe pero no estado
        if (fecha_i != "" and fecha_f != "" and estado=="4"):  # existen rangos de fechas
            if (articulo != ""):
                nr = ReservaArticulo.objects.exclude(fecha_inicial=fecha_i, fecha_final=fecha_f)
                # inventario = nr.all().select_related('articulo')
                inventario = Articulo.objects.filter(nombre__iexact=articulo)

                try:
                    inventarioId = Articulo.objects.filter(pk=articulo)
                    inventario = inventario.union(inventarioId)
                except ValueError:
                    pass
            else:
                # inventario = n.select_related('articulo')
                inventario = Articulo.objects.all()

        elif (fecha_i != "" and fecha_f != "" and estado != "4"):
            if (articulo != ""):
                nr = ReservaArticulo.objects.exclude(fecha_inicial=fecha_i, fecha_final=fecha_f)
                # inventario = nr.all().select_related('articulo').filter(nombre__iexact=articulo, estado=estado)
                inventario = Articulo.objects.filter(nombre__iexact=articulo, estado=estado)

                try:
                    inventarioId = Articulo.objects.filter(pk=articulo)
                    inventario = inventario.union(inventarioId)
                except ValueError:
                    pass

            else:
                # inventario = nr.all().select_related('articulo').filter(estado=estado)
                inventario = Articulo.objects.filter(estado=estado)

        # campo estado existe pero no fechas
        elif (estado != "4"):
            if (articulo != ""):
                inventario = Articulo.objects.filter(nombre__iexact=articulo, estado=estado)

                try:
                    inventarioId = Articulo.objects.filter(pk=articulo, estado=estado)
                    inventario = inventario.union(inventarioId)
                except ValueError:
                    pass

            else:
                inventario = Articulo.objects.filter(estado=estado)

        # campo articulo pero no estado ni fechas
        elif (articulo != ""):
            inventario = Articulo.objects.filter(nombre__iexact=articulo)
            try:
                inventarioId = Articulo.objects.filter(pk=articulo)
                inventario = inventario.union(inventarioId)
            except ValueError:
                pass

        # Ningun campo existe
        else:
            inventario = Articulo.objects.all()

        return render(request, 'reservasApp/listaArticulos.html', {'articulos': inventario})

    else:
        articulos = Articulo.objects.all()

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
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('reservasApp:listaArt')
    else:
        form = LoginForm()
    return render(request, 'reservasApp/login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect('reservasApp:listaArt')




def fichaArticulo(request):
    if request.user.is_superuser:
        a=1
    else:
        a=0
    articulo_id = request.GET['idart']
    art = get_object_or_404(Articulo, id=articulo_id)
    nombre = art.nombre
    estado = art.estado
    descripcion = art.descripcion
    foto = get_object_or_404(FotoArticulo, articulo=articulo_id)
    reservas = ReservaArticulo.objects.filter(articulo=art)
    context = {'nombre': nombre, 'estado': estado, 'descripcion': descripcion, 'idarticulo': articulo_id, 'foto': foto, 'reservas': reservas, 'admin': a}
        # context = {'nombre': nombre, 'estado': estado, 'descripcion': descripcion, 'idarticulo': articulo_id, 'foto': foto}
    return render(request, 'reservasApp/fichaArticulo.html', context)

def editArticulo(request):
    if request.method == 'GET':
        articulo_id = request.GET['idart']
        art = get_object_or_404(Articulo, id=articulo_id)
        nombre = art.nombre
        descripcion = art.descripcion
        context = {'nombre': nombre, 'idart': articulo_id, 'descripcion': descripcion}
        return render(request, 'reservasApp/editArticulo.html', context)
    else:
        return HttpResponse("Error al editar")

def nuevosDatos(request):
    if request.method == 'POST':
        articulo_id = request.POST['idart']
        art = get_object_or_404(Articulo, id=articulo_id)
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        estado = request.POST['estado']
        art.nombre= nombre
        art.descripcion = descripcion
        es=0
        if(estado == "Disponible"):
            es=1
        elif(estado == "En prestamo"):
            es=2
        elif(estado == "Perdido"):
            es=3
        art.estado = es
        art.save()
        return redirect('/fichaArticulo?idart=' + articulo_id)
    else:
        return HttpResponse("Error al actualizar datos")



def exito(request):
    if request.method == 'POST':
        usr = request.user
        usrid = usr.id
        idarticulo = request.POST['id_articulo']
        fecha_i = request.POST['fecha_i']
        fecha_f = request.POST['fecha_f']
        hora_i = request.POST['hora_i']
        hora_f = request.POST['hora_f']
        art = get_object_or_404(Articulo, id=idarticulo)

        nuevo = ReservaArticulo(id_usuario=usrid, articulo=art, fecha_inicial=fecha_i, fecha_final=fecha_f, hora_inicial=hora_i,
                            hora_final=hora_f, estado=2)
        #if nuevo.fecha_inicial.weekday() == 5 | nuevo.fecha_inicial.weekday() == 6:
        #    return HttpResponse("No se puede reservar en fin de semana")
        #if nuevo.fecha_final.weekday() == 5 | nuevo.fecha_final.weekday() == 6:
         #   return HttpResponse("No se puede reservar en fin de semana")

        nuevo.save()
    return render(request, 'reservasApp/exito.html')


def perfil(request):
    if (request.user.is_authenticated):
        if (request.user.groups.filter(name='Administrador').exists()):
            reservasesp = sorted(ReservaEspacio.objects.all() , key=attrgetter('fecha_reserva'), reverse=True)
            reservasart = sorted(ReservaArticulo.objects.all() , key=attrgetter('fecha_reserva'), reverse=True)
            reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'), reverse=True)
            reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
            context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
            return render(request, 'reservasApp/perfiladmin.html', context)
        else:
            reservasesp = sorted(ReservaEspacio.objects.filter(id_usuario=request.user.id), key=attrgetter('fecha_reserva'), reverse=True)
            reservasart = sorted(ReservaArticulo.objects.filter(id_usuario=request.user.id), key=attrgetter('fecha_reserva'), reverse=True)
            reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
            reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)[:10]
            context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
            return render(request, 'reservasApp/perfil.html', context)

def eliminar_pendientesesp(request):
    for i in request.POST.getlist("reserva"):
        ReservaEspacio.objects.filter(id=i).delete()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfil.html', context)

def eliminar_pendientesart(request):
    for i in request.POST.getlist("reserva"):
        ReservaArticulo.objects.filter(id=i).delete()
    reservasesp = ReservaEspacio.objects.all()
    reservasart = ReservaArticulo.objects.all()
    reservas = sorted(chain(reservasesp, reservasart), key=attrgetter('fecha_reserva'))
    reservas_recientes = sorted(reservas, key=attrgetter('fecha_reserva'), reverse=True)
    context  = {'reservas_recientes': reservas_recientes, 'reservas': reservas, 'reservasart': reservasart, 'reservasesp':reservasesp}
    return render(request, 'reservasApp/perfil.html', context)

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
