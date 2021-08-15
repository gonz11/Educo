from django.contrib import admin
from turno.models import Turno
from turno.models import DetalleTurno
# Register your models here.
class TurnoAdmin(admin.ModelAdmin):
    list_filter = ['alumno__legajo', 'alumno__nombre','alumno__apellido','alumno__dni','alumno__usuario__email','estadoTurno__nombre']


admin.site.register(Turno,TurnoAdmin)
admin.site.register(DetalleTurno)
