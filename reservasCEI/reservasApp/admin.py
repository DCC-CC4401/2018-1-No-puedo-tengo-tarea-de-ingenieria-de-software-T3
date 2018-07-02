from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Articulo)
admin.site.register(Espacio)
admin.site.register(ReservaArticulo)
admin.site.register(ReservaEspacio)
admin.site.register(FotoArticulo)
admin.site.register(FotoEspacio)

