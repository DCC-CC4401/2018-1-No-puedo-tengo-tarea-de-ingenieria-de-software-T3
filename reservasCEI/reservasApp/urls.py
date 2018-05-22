from django.urls import path, re_path
from django.conf import settings
from . import views

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.listaArticulos, name='index'),
    re_path(r'^espacios/$', views.espacios, name='espacios'),
    path('articulos', views.listaArticulos, name='listaArt'),
    path('busquedaAvanzada', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('busquedaSimple', views.busquedaSimple, name='busquedaSimple'),
    re_path(r'^reservas/$', views.reservas, name='reservas'),
    path('crearUsuario', views.crearUsuario, name='crearUsuario'),
    path('logout', views.logoutView, name='logout'),
    path('login', views.loginView, name='login'),
]
