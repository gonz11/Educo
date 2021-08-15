from django.conf.urls import  url
from django.contrib.auth.decorators import login_required

from pago.views import ComprarLibros

urlpatterns = [
    url(r'^comprar_libros/$', login_required(ComprarLibros), name='comprar_libros'),
]