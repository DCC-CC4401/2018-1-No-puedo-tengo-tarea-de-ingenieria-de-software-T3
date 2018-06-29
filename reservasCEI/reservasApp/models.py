from django.db import models

# Create your models here.

class Articulo (models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.IntegerField() # 0 en reparación, 1 disponible, 2 en préstamo (Cambiar por listas)
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class Espacio (models.Model):
    nombre = models.CharField(max_length=200)
    capacidad = models.IntegerField(default=0)
    descripcion = models.TextField()
    estado = models.IntegerField(default=1) # 0 en reparación, 1 disponible, 2 en préstamo (Cambiar por listas)
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class FotoArticulo (models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    ruta = models.ImageField(blank=True, null=True)

class FotoEspacio (models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    ruta = models.ImageField(blank=True, null=True)

class ReservaArticulo (models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final = models.TimeField(blank=True, null=True)
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() # 0 rechazada, 1 aprobada, 2 pendiente

class ReservaEspacio (models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_inicial = models.DateTimeField(blank=True, null=True)
    fecha_final = models.DateTimeField(blank=True, null=True)
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() # 0 rechazada, 1 aprobada, 2 pendiente
