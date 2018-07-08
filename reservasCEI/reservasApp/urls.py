from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.listaArticulos, name='index'),
    path('articulos', views.listaArticulos, name='listaArt'),
    path('spaces', views.listaEspacios, name='listaEsp'),
    path('exito', views.exito, name='exito'),
    path('editnombre', views.perfil, name='editnombre'),
    path('editestado', views.perfil, name='editestado'),
    path('editdesc', views.perfil, name='editdesc'),
    path('perfil', views.perfil, name='perfil'),


    path('busquedaAvanzada', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('busquedaSimple', views.busquedaSimple, name='busquedaSimple'), #cambiar url por id

    path('crearUsuario', views.crearUsuario, name='crearUsuario'),
    path('logout', views.logoutView, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'reservasApp/login.html'}, name='login'),
    path('fichaArticulo', views.fichaArticulo, name='fichaArticulo'),
    path('eliminar_pendientesart', views.eliminar_pendientesart, name='eliminar_pendientesart'),
    path('eliminar_pendientesesp', views.eliminar_pendientesesp, name='eliminar_pendientesesp'),
    path('aprobarart', views.aprobarart, name='aprobarart'),
    path('rechazarart', views.rechazarart, name='rechazarart'),
    path('aprobaresp', views.aprobaresp, name='aprobaresp'),
    path('rechazaresp', views.rechazaresp, name='rechazarsep'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
