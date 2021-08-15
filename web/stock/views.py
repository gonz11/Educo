from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from stock.models import Libro
from turno.models import Creado, Turno, DetalleTurno, PorRetirar, Retirado


def ElegirLibros(request):
    query = request.GET.get("query","")
    if query:
        q = Q(titulo__icontains = query)
        q |= Q(autor__nombre__icontains = query)
        q |= Q(autor__apellido__icontains = query)
        q |= Q(autor__nacionalidad__name__icontains = query)
        q |= Q(descripcion__icontains = query)

        libros = Libro.objects.filter(q)
    else:
        libros = Libro.objects.all()
    return render(request,'elegir_libros.html',{"libros":libros,"query":query})

def AgregarLibro(request,id_libro):
    alumno = request.user.get_alumno()
    if Turno.objects.filter(estadoTurno = Creado.objects.all().first(),alumno=alumno).exists():
        turno = Turno.objects.get(estadoTurno = Creado.objects.all().first(),alumno=alumno)
    else:
        turno = Turno.objects.create(estadoTurno=Creado.objects.all().first(),alumno=alumno)
    turno.add_detalle(id_libro)
    return HttpResponseRedirect(reverse("elegir_libros"))

def QuitarLibro(request,id_libro):
    alumno = request.user.get_alumno()
    detalle = DetalleTurno.objects.get(turno__estadoTurno = Creado.objects.all().first(),turno__alumno=alumno,ejemplar__libro_id=id_libro)
    detalle.delete()
    return HttpResponseRedirect(reverse("libros_elegidos"))


def LibrosElegidos(request):
    if Turno.objects.filter(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first()).exists():
        turno = Turno.objects.get(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())
    else:
        turno = Turno.objects.create(alumno=request.user.get_alumno(),estadoTurno=Creado.objects.all().first())
    return render(request,"libros_elegidos.html",{"turno":turno})


def LibrosMasVendidos(request):
    libros = DetalleTurno.objects.filter(turno__estadoTurno__in=[PorRetirar.objects.all().first(),Retirado.objects.all().first()]).values('ejemplar__libro__titulo').annotate(cant=Sum('cantidad'))
    return render(request,'libros_mas_vendidos.html',{"libros":libros})