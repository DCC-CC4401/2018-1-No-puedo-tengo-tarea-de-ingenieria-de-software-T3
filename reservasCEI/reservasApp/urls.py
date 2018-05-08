from django.urls import path
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('administrar/pendientes', views.adminPendientes, name='resPend'),
    path('listaArticulos', views.listaArticulos, name = 'listaArt'),
    path('listaArticulos/avanzada', views.listArtAvan, name='listArtAvan'),
]
#if settings.DEBUG:
#    urlpatterns += [
#        path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
#        ]
