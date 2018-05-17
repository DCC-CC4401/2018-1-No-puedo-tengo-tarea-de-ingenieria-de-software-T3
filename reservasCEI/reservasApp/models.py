from django.db import models
from datetime import *

ESTADO = (
    (0, 'Perdido'),
    (1, 'Disponible'),
    (2, 'En Préstamo'),
    (3, 'Perdido o Inutilizable'),
)

RESERVA_ESTADO = (
    (0, 'Rechazada'),
    (1, 'Aprobada'),
    (2, 'Pendiente'),
)

class Articulo (models.Model):
    nombre = models.CharField(max_length=200)
    foto = models.ImageField(blank=True)
    descripcion = models.TextField()
    estado = models.IntegerField(choices=ESTADO, default=1)
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class Espacio (models.Model):
    nombre = models.CharField(max_length=200)
    foto = models.ImageField(blank=True)
    capacidad = models.IntegerField()
    descripcion = models.TextField()
    estado = models.IntegerField(choices=ESTADO, default=1)
    def __str__(self):
        return self.nombre

class ReservaArticulo (models.Model):
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField() # por defecto 1 hora mas es algo como esto:
                                         # blank=True, default=fecha_inicial + timedelta(hours = 1))
    estado = models.IntegerField(choices=RESERVA_ESTADO, default=2)

class ReservaEspacio (models.Model):
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField()
    estado = models.IntegerField(choices=RESERVA_ESTADO, default=2)
    def __str__(self):
        return str(self.espacio) + ' - ' + str(self.estado)

#class FotoArticulo (models.Model):
    #articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    #ruta = models.ImageField(blank=True, null=True)

#class FotoEspacio (models.Model):
#    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
#    ruta = models.ImageField(blank=True, null=True)
