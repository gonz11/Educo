from django.contrib import admin

from stock.models import Libro
from stock.models import Autor
from stock.models import Proveedor
from stock.models import Ejemplar

# Register your models here.
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Proveedor)
admin.site.register(Ejemplar)
