from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.dateparse import parse_datetime

from pago.models import Compra
from turno.models import Turno, Creado, PorRetirar


def ElegirTurno(request):
    fecha=request.GET.get("fecha")
    id_turno=request.GET.get("id_turno")
    if fecha:
        if id_turno:
            turno = Turno.objects.get(id=id_turno)
        else:
            turno = Turno.objects.get(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())
        if Compra.objects.filter(turno=turno).exists():
            turno.fechaTurno = parse_datetime(fecha)
            turno.estadoTurno = PorRetirar.objects.all().first()
            turno.save()
            return HttpResponseRedirect(reverse("mis_turnos"))
    dias=[]
    minutos=["00","10","20","30","40","50"]
    horas=["09","10","11","12","13","14","15","16","17","18","19","20"]
    for i in range(1,10):
        dia= datetime.now()+timedelta(days=i)
        if dia.weekday()!=5 and dia.weekday()!=6:
            h = []
            for hora in horas:
                for minuto in minutos:
                    if not Turno.objects.filter(fechaTurno__year=dia.year,fechaTurno__month=dia.month,fechaTurno__day=dia.day,fechaTurno__regex=hora+":"+minuto).exists():
                        h.append(hora+":"+minuto)
            dias.append({
                "dia":dia,
                "horas":h
            })
    return render(request,"elegir_turno.html",{"dias":dias,"id_turno":id_turno})

def MisTurnos(request):
    return render(request,'mis_turnos.html',{"turnos":Turno.objects.filter(alumno=request.user.get_alumno())})