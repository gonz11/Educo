from django.conf.urls import  url
from django.contrib.auth.decorators import login_required

from stock.views import LibrosMasVendidos
from turno.views import ElegirTurno, MisTurnos

urlpatterns = [
    url(r'^elegir/turno/$', login_required(ElegirTurno), name='elegir_turno'),
    url(r'^mis/turnos/$', login_required(MisTurnos), name='mis_turnos'),
    url(r'^libros/mas/vendidos/$', login_required(LibrosMasVendidos), name='libros_mas_vendidos'),
]
