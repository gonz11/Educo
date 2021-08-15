from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View

from alumno.emails import email_verify_password, email_welcome
from alumno.forms import MyUserForm, LoginForm
from alumno.models import User, CodeValidator, _generate_code, Alumno


class SignupView(FormView):
    template_name = 'home_signup.html'
    form_class = MyUserForm

    def get(self, request,**kwargs):
        return render(request,self.template_name,{'form':MyUserForm(),})

    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['apellido']
        legajo = form.cleaned_data['legajo']
        dni = form.cleaned_data['dni']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.filter(email=email)
        if len(user)==0:
            user = User.objects.create_user(email=email,usuario=email, password=password, verify_email=False)
            Alumno.objects.create(nombre=nombre,apellido=apellido,legajo=legajo,dni=dni,usuario=user)
        else:
            user=user[0]
            if user.verify_email:
                form.add_error("email","El email ya se encuentra registrado")
                return super(SignupView, self).form_invalid(form)
            else:
                code = CodeValidator.objects.filter(user=user)
                code.delete()

        code = CodeValidator(code=_generate_code(), user=user)
        code.save()

        email_verify_password(code,user)

        return super(SignupView, self).form_valid(form)

    def get_success_url(self):
        return reverse('signup_email_sent_page')


class SignupEmailSentView(TemplateView):
    template_name = 'home_signup_email_sent.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})



class SignupVerifyView(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')
        code_validator = CodeValidator.objects.filter(code=code)
        # Handle other error responses from API
        if len(code_validator)!=1:
            return HttpResponseRedirect(reverse('signup_not_verified_page'))

        user = code_validator.first().user.activate_email()

        code = CodeValidator.objects.filter(user=user)
        code.delete()

        email_welcome(user)

        return HttpResponseRedirect(reverse('signup_verified_page'))

def LoginView(request):
    template_name = 'home_login.html'
    form_class = LoginForm
    is_staff = False

    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect(reverse('elegir_libros'))

    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user is not None and user.verify_email:
                if not user.is_active:
                    user.set_is_active(True)
                    user.save()
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return HttpResponseRedirect(next)
                else :
                    return HttpResponseRedirect(reverse('elegir_libros'))
            else:
                # Return an 'invalid login' error message.
                form.add_error("email","El email o password son invalidos")
    else:
        form = LoginForm()

    return render(request,template_name,{'form':form,})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login_page'))

class SignupNotVerified(TemplateView):
    template_name = 'home_signup_not_verified.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})


class SignupVerified(TemplateView):
    template_name = 'home_signup_verified.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})
