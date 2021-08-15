from django.contrib import admin
from pago.models import Devolucion
from pago.models import Compra

class CompraAdmin(admin.ModelAdmin):
    list_filter = ['fechaCompra','turno__alumno__legajo', 'turno__alumno__nombre','turno__alumno__apellido','turno__alumno__dni','turno__alumno__usuario__email','turno__estadoTurno__nombre']

# Register your models here.
admin.site.register(Devolucion)
admin.site.register(Compra,CompraAdmin)
