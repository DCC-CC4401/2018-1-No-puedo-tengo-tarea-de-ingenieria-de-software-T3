from django.urls import path, re_path
from django.conf import settings
from . import views

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^espacios/$', views.espacios, name='espacios'),
    re_path(r'^espacios/(?P<espacio_id>[0-9]+)$', views.fichaEspacio, name='fichaEspacio'),
    path('articulos', views.listaArticulos, name = 'listaArt'),
    path('busquedaAvanzada', views.busquedaAvanzada),
    path('busquedaSimple', views.busquedaSimple)
]
