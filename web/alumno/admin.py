from django.contrib import admin
from alumno.models import Alumno, User

# Register your models here.
class AlumnoAdmin(admin.ModelAdmin):
    search_fields = ['legajo', 'nombre','apellido','dni','usuario__email']

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email',]

admin.site.register(Alumno,AlumnoAdmin)
admin.site.register(User,UserAdmin)
