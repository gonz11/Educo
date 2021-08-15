# Educo
Aplicacion web con Python, Django, HTML y CSS.
Este es un sistema de reserva de libros para alumnos donde se pueden elegir uno o varios libros 
para retirar y elegir un turno para retirarlos. Ademas el alumno puede crear un usuario y 
logearse en el sistema. 



# Iniciar app
- sudo docker-compose build
- sudo docker-compose run web python manage.py createsuperuser
- sudo docker-compose up
- Acceder al navegador e ingresar a la direccion localhost:8080 o 0.0.0.0:8080 
  (Si no accede, entrar al archivo docker-compose y cambiar en la seccion ports del servicio
 web a "8080:8080" o "8080"). 

