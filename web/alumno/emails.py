import os

from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def email_verify_password(code,user):
    url =  Site.objects.get_current().domain + reverse('signup_verify') + '?code=' + str(code.code)
    context = {'name': user.get_alumno().nombre,'url': url, 'company':"Educo",'site_root':Site.objects.get_current().domain}

    message_html = get_template("email/home_signup.html").render(context)
    subject = "Hola " + user.get_alumno().nombre + ". Por favor confirma tu correo electrónico."
    message = get_template("email/home_signup.txt").render(context)

    send_email_hola(email=user.email, subject=subject,message=message, message_html=message_html)



def email_welcome(user):
    context = {'name': user.get_alumno().nombre,'site_root':  Site.objects.get_current().domain,
               'company':"Educo"}

    message_html = get_template("email/home_welcome.html").render(context)
    subject = "Hola " + user.get_alumno().nombre + ". Te damos la bienvenida a Educo."
    message = get_template("email/home_welcome.txt").render(context)

    send_email_hola(email=user.get_email(), subject=subject,message=message, message_html=message_html)


def send_email_hola(email, subject,message, message_html,from_email="Company",user=None):
    send_email(email,subject,message,message_html,from_email,settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)


def send_email(email,subject,message,message_html,from_email,auth_user,auth_password,user=None):
    if user == None or (user != None and user.subscribe_email):
        if not settings.DEBUG:
            send_mail(subject=subject,message=message, from_email=auth_user,auth_user=auth_user,auth_password=auth_password,
                      recipient_list=[email] ,fail_silently=True,html_message=message_html)
        else:
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, auth_user=settings.EMAIL_HOST_USER,
                      auth_password=settings.EMAIL_HOST_PASSWORD,
                      recipient_list=[email], fail_silently=False, html_message=message_html)
