from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from . import views

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.listaArticulos, name='index'),
    path('articulos', views.listaArticulos, name='listaArt'),
    path('spaces', views.listaEspacios, name='listaEsp'),
    path('exito', views.exito, name='exito'),
    path('perfil', views.perfil, name='perfil'),

    path('busquedaAvanzada', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('busquedaSimple', views.busquedaSimple, name='busquedaSimple'), #cambiar url por id

    re_path(r'^reservas/$', views.reservas, name='reservas'),
    path('crearUsuario', views.crearUsuario, name='crearUsuario'),
    path('logout', views.logoutView, name='logout'),
    path('login', views.loginView, name='login'),
    path('fichaArticulo', views.fichaArticulo, name='fichaArticulo'),
    path('eliminar_pendientesart', views.eliminar_pendientesart, name='eliminar_pendientesart'),
    path('eliminar_pendientesesp', views.eliminar_pendientesesp, name='eliminar_pendientesesp'),
    path('aprobarart', views.aprobarart, name='aprobarart'),
    path('rechazarart', views.rechazarart, name='rechazarart'),
    path('aprobaresp', views.aprobaresp, name='aprobaresp'),
    path('rechazaresp', views.rechazaresp, name='rechazarsep'),
]
