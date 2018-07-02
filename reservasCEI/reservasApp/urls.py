from django.urls import path, re_path
from django.conf import settings
<<<<<<< HEAD
=======
from django.views.static import serve

>>>>>>> ilana
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
]

