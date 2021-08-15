from django.db import models

# Create your models here.
from alumno.models import Alumno
from stock.models import Ejemplar
from model_utils.managers import InheritanceManager


class Turno (models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    estadoTurno = models.ForeignKey('EstadoTurno', on_delete=models.CASCADE)
    fechaTurno = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "%s %s - %s - Fecha:%s" %(self.alumno.nombre,self.alumno.apellido,self.estadoTurno.nombre, self.get_fecha_turno_str())

    def get_hora(self):
        return "%02d" %self.fechaTurno.hour if self.fechaTurno else "No asignado"

    def get_minuto(self):
        return "%02d"%(self.fechaTurno.minute) if self.fechaTurno else ""

    def get_compra(self):
        from pago.models import Compra
        return Compra.objects.filter(turno=self).first()

    def get_fecha_turno_str(self):
        return str(self.fechaTurno) if self.fechaTurno else "No asiganda"

    def get_estado(self):
        return EstadoTurno.objects.get_subclass(id=self.estadoTurno.id)

    def add_detalle(self,id_libro):
        DetalleTurno.objects.create(ejemplar=Ejemplar.objects.filter(cantidad__gt=0,libro_id=id_libro).first(),cantidad=1,turno=self)

    def get_detalles(self):
        return DetalleTurno.objects.filter(turno=self)

    def comprar(self,metodo_pago):
        self.get_estado().comprar(self,metodo_pago)

    def total(self):
        total=0
        for detalle in self.get_detalles():
            total+=detalle.ejemplar.precio
        return total

class DetalleTurno (models.Model):
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %iun - %s" %(self.ejemplar.libro.titulo,self.cantidad,self.turno.__str__())

class EstadoTurno(models.Model):
    nombre = models.CharField(max_length=50)
    objects = InheritanceManager()
    def __str__(self):
        return self.nombre

    def esPorRetirar(self):
       return False
    def esRetirado(self):
       return False
    def esCancelado(self):
       return False
    def esCreado(self):
       return False
    def comprar(self,turno,metodo_pago):
        pass


class Creado (EstadoTurno):
   def esPorRetirar(self):
       return True
   def esRetirado(self):
       return False
   def esCancelado(self):
       return False
   def esCreado(self):
       return True
   def comprar(self,turno,metodo_pago):
        for detalle in turno.get_detalles():
            detalle.ejemplar.cantidad= detalle.ejemplar.cantidad - detalle.cantidad
            detalle.ejemplar.save()
        from pago.models import Compra
        Compra.objects.create(turno=turno,metodoPago_id=metodo_pago,precioTotal=turno.total())
        turno.save()

class PorRetirar (EstadoTurno):
   def esPorRetirar(self):
       return True
   def esRetirado(self):
       return False
   def esCancelado(self):
       return False
   def esCreado(self):
    return False
   def comprar(self,turno,metodo_pago):
        pass


class Retirado (EstadoTurno):
   def esPorRetirar(self):
       return False
   def esRetirado(self):
       return True
   def esCancelado(self):
       return False
   def esCreado(self):
       return False
   def comprar(self,turno,metodo_pago):
        pass


class Cancelado (EstadoTurno):
    def esPorRetirar(self):
       return False
    def esRetirado(self):
       return False
    def esCancelado(self):
       return True
    def esCreado(self):
       return False
    def comprar(self,turno,metodo_pago):
        pass
