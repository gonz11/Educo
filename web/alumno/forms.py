from django import forms
from django.forms.forms import NON_FIELD_ERRORS


class MyUserForm(forms.Form):
        email = forms.EmailField(widget=forms.TextInput(attrs={'required': True,'class': 'form-control b-r-xl', 'type':'email'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
        legajo = forms.IntegerField(widget=forms.NumberInput(attrs={'required': True,'class': 'form-control b-r-xl'}))
        nombre = forms.CharField(widget=forms.TextInput(attrs={'required': True,'class': 'form-control b-r-xl'}))
        apellido = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control b-r-xl'}))
        dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control b-r-xl'}))


class AddErrorMixin(object):
    def add_error(self, field, msg):
        field = field or NON_FIELD_ERRORS
        if field in self._errors:
            self._errors[field].append(msg)
        else:
            self._errors[field] = self.error_class([msg])

class PasswordForm(AddErrorMixin, forms.Form):

    password = forms.CharField(max_length=128, widget=forms.TextInput(attrs={"type":"password","class":"center-block campo-form ",
                                                           "placeholder":"Password","required":True}))


class SignupForm(PasswordForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"type":"text",
                                                                                             "class":"center-block campo-form",
                                                                                             "placeholder":"Nombre",
                                                                                             "required":True}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={"type":"email",
                                                                           "class":"center-block campo-form",
                                                                            "placeholder":"E-mail",
                                                                           "required":True}))


class LoginForm(AddErrorMixin, forms.Form):
    email = forms.EmailField(max_length=255,widget=forms.TextInput(attrs={"type":"email","class":"form-control",
                                                           "placeholder":"E-mail","required":True}))
    password = forms.CharField(max_length=128,widget=forms.TextInput(attrs={"type":"password","class":"form-control",
                                                           "placeholder":"Password","required":True}))


class PasswordResetForm(AddErrorMixin, forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={"type":"email",
                                                                           "class":"center-block campo-form form-control",
                                                                           "placeholder":"E-mail",
                                                                           "required":True}))

class PasswordResetVerifiedForm(PasswordForm):
    pass

class PasswordChangeForm(PasswordForm):
    password = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={"type": "password", "class": "form-control",
                                                             "placeholder": "Nueva contraseña", "required": True}))
    password2 = forms.CharField(max_length=128,
                                widget=forms.TextInput(attrs={"type": "password", "class": "form-control",
                                                              "placeholder": "Confirma tu nueva contraseña", "required": True}))
