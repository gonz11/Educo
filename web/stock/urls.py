from django.conf.urls import  url
from django.contrib.auth.decorators import login_required

from stock.views import ElegirLibros, AgregarLibro, QuitarLibro, LibrosElegidos

urlpatterns = [
    url(r'^elegir/libros/$', login_required(ElegirLibros), name='elegir_libros'),
    url(r'^agregar/libro/(?P<id_libro>(\d*))/$', login_required(AgregarLibro), name='agregar_libro'),
    url(r'^quitar/libro/(?P<id_libro>(\d*))/$', login_required(QuitarLibro), name='quitar_libro'),
    url(r'^libros/elegidos/$', login_required(LibrosElegidos), name='libros_elegidos'),

]
