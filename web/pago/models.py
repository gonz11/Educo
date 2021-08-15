from django.db import models

# Create your models here.
from turno.models import Turno


class Devolucion (models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=256)
    fechaDevolucion = models.DateField(auto_now=True) # se pone sola la fecha

    class Meta:
        verbose_name="Devolucion"
        verbose_name_plural="Devoluciones"

class Compra (models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    metodoPago = models.ForeignKey('MetodoPago',on_delete=models.CASCADE)
    fechaCompra = models.DateField(auto_now=True) # se pone sola la fecha
    precioTotal = models.FloatField()

    def __str__(self):
        return "%s - Metodo de pago:%s - Fecha de compra:%s - Precio total: %f" %(self.turno.alumno.__str__(),self.metodoPago.descripcion,self.fechaCompra, self.precioTotal)

class MetodoPago (models.Model):
    descripcion = models.CharField(max_length=256)

    def __str__(self):
        return self.descripcion