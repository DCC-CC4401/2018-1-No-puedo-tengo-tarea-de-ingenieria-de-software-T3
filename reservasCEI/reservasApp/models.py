from django.db import models
from datetime import *
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User

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


class Articulo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.IntegerField(choices=ESTADO, default=1) #0 en reparacion, 1 disponible, 2 en prestamo, 3 perdido

    def __str__(self):
        return self.nombre


class Espacio(models.Model):
    nombre = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    descripcion = models.TextField()
    estado = models.IntegerField(choices=ESTADO, default=1)

    def __str__(self):
        return self.nombre


class ReservaArticulo(models.Model):
    # id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(default=datetime.now())
    fecha_inicial = models.DateField()
    hora_inicial = models.IntegerField(validators=[MaxValueValidator(17), MinValueValidator(9)])
    fecha_final = models.DateField()
    hora_final = models.IntegerField(validators=[MaxValueValidator(18), MinValueValidator(10)])
    estado = models.IntegerField(choices=RESERVA_ESTADO, default=2)

    def __str__(self):
        return str(self.articulo)

    def get_estado(self):
        return RESERVA_ESTADO[self.estado][1]


class ReservaEspacio(models.Model):
    # id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(default=datetime.now())
    fecha_inicial = models.DateField()
    hora_inicial = models.IntegerField(validators=[MaxValueValidator(17), MinValueValidator(9)])
    fecha_final = models.DateField()
    hora_final = models.IntegerField(validators=[MaxValueValidator(18), MinValueValidator(10)])
    estado = models.IntegerField(choices=RESERVA_ESTADO, default=2)

    def __str__(self):
        return str(self.espacio)

    def get_estado(self):
        return RESERVA_ESTADO[self.estado][1]


class FotoArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    ruta = models.ImageField(blank=True)


class FotoEspacio(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    ruta = models.ImageField(blank=True)


'''
Usuarios
'''


class Person(User):

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self._meta.get_field('username').validators = [RegexValidator(
            regex='\d(\d?)[.](\d{3})[.](\d{3})[-](\d|[kK])$',
            message='Debe ingresar el rut con puntos y digito verificador. (Por ejemplo: 12.345.678-9)',
            code='invalid-username'), ]

    class Meta:
        proxy = True
