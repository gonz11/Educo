# Create your models here.
from django.db import models
from cities_light.models import Country

class Autor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    nacionalidad = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        verbose_name="Autor"
        verbose_name_plural="Autores"

    def __str__(self):
        return "%s %s - %s" %(self.nombre,self.apellido,self.nacionalidad)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=30)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30)
    class Meta:
        verbose_name="Proveedor"
        verbose_name_plural="Provedores"

    def __str__(self):
        return "%s" %self.nombre

class Libro (models.Model):
    titulo = models.CharField(max_length=30)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    descripcion = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s %s" %(self.titulo,self.autor.nombre, self.autor.apellido)

    def get_cantidad(self):
        from django.db.models import Sum
        return Ejemplar.objects.filter(libro=self).aggregate(cantidad=Sum("cantidad"))["cantidad"]

class Ejemplar(models.Model):
    cantidad = models.IntegerField()
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio = models.FloatField()
    class Meta:
        verbose_name="Ejemplar"
        verbose_name_plural="Ejemplares"

    def __str__(self):
        return "%s - %iun - $%s - %s" %(self.libro.titulo,self.cantidad,'{0:.2f}'.format(self.precio),self.proveedor.nombre)