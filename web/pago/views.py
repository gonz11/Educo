from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from turno.models import Turno, Creado, DetalleTurno


def ComprarLibros(request):
    if( not Turno.objects.filter(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first()).exists() or
        not DetalleTurno.objects.filter(turno = Turno.objects.get(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())).exists()):
        return HttpResponseRedirect(reverse("elegir_libros"))

    if request.method=="POST":
        turno = Turno.objects.get(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())
        turno.comprar(1)
        return HttpResponseRedirect(reverse("elegir_turno"))
    return render(request,'comprar_libros.html',{"turno":Turno.objects.get(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())})