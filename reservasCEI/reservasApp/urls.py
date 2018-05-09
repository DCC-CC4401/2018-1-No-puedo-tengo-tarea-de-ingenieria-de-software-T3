from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from . import views

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^espacios/$', views.espacios, name='espacios'),
    re_path(r'^espacios/(?P<espacio_id>[0-9]+)$', views.fichaEspacio, name='fichaEspacio'),
    re_path(r'^cambiarespacio/$', views.cambiarespacio, name='cambiarespacio'),
    path('listaArticulos', views.listaArticulos, name = 'listaArt'),
    path('listaArticulos/avanzada', views.listArtAvan, name='listArtAvan'),
]
#if settings.DEBUG:
#    urlpatterns += [
#        path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
#        ]
