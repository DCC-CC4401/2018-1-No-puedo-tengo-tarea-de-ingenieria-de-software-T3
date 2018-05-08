from django.db import models

# Create your models here.

class Articulo (models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.IntegerField() # 0 no disponible, 1 disponible, 2 en reparación, otros?
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class Espacio (models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.IntegerField() # 0 no disponible, 1 disponible, 2 en reparación, otros?
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class FotoArticulo (models.Model):
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    #foto = models.ImageField()

class FotoEspacio (models.Model):
    id_espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    #foto = models.ImageField()

class ReservaArticulo (models.Model):
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField()
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() # 0 rechazada, 1 aprobada, 2 pendiente

class ReservaEspacio (models.Model):
    id_espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_inicial = models.DateTimeField()
    fecha_final = models.DateTimeField()
    #id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() # 0 rechazada, 1 aprobada, 2 pendiente
