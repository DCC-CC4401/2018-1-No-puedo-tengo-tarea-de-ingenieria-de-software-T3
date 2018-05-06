from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('administrar/pendientes', views.adminPendientes, name='resPend'),
    path('listaArticulos', views.listaArticulos, name = 'listaArt')
]