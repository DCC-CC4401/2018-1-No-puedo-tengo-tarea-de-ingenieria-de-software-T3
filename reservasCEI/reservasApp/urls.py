from django.urls import path, re_path
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'reservasApp'

urlpatterns = [
    re_path(r'^$', views.listaArticulos, name='index'),
    re_path(r'^espacios/$', views.espacios, name='espacios'),
    path('articulos', views.listaArticulos, name='listaArt'), #agregar expresion regular para las imagenes y luego cargar esto en el view

    path('articulos', views.imagenesArticulos, name='imgArt'),

    path('busquedaAvanzada', views.busquedaAvanzada, name='busquedaAvanzada'),
    path('busquedaSimple', views.busquedaSimple, name='busquedaSimple'), #cambiar url por id

    re_path(r'^reservas/$', views.reservas, name='reservas'),
    path('crearUsuario', views.crearUsuario, name='crearUsuario'),
    path('logout', views.logoutView, name='logout'),
    path('login', views.loginView, name='login'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
