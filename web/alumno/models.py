from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
import binascii
import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


def _generate_code():
    return binascii.hexlify(os.urandom(20))

class UserManager(BaseUserManager):
    def _create_user(self, usuario, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not usuario:
            raise ValueError(_('El email es necesario'))
        email = self.normalize_email(email)
        user = self.model(usuario=usuario, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, usuario, email=None, password=None, **extra_fields):
        #Verify exist email
        email = self.normalize_email(email)
        if email!=None:
            user = User.objects.filter(email=email)
            if len(user)==1:
                return user[0]

        return self._create_user(usuario, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, usuario, email, password, **extra_fields):
        user = self._create_user(usuario, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    usuario = models.CharField(_('usuario'), max_length=255, unique=True,
                                help_text=_(
                                    'Campo requerido'),
                                )
    email = models.EmailField(_('email'), max_length=255)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    verify_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_date_joined(self):
        return self.date_joined

    def set_data(self,first_name,last_name):
        self.first_name=first_name
        self.last_name = last_name
        self.save()

    def get_is_active(self):
        return self.is_active

    def get_is_staff(self):
        return self.is_staff

    def set_is_active(self,is_active):
        self.is_active = is_active
        self.save()

    def get_email(self):
        return self.email

    def get_username(self):
        return self.usuario

    def activate_email(self):
        self.verify_email = True
        self.is_active = True
        self.save(force_update=True,update_fields=['verify_email','is_active'])
        return self

    def _get_pk_val(self, meta=None):
        if not meta:
            meta = self._meta
        try:
            return getattr(self, meta.pk.attname)
        except AttributeError:
            return None

    def set_email(self,email):
        self.email = email

    def set_verify_email(self,verify_email):
        self.verify_email = verify_email

    def get_alumno(self):
        return Alumno.objects.get(usuario=self)


class CodeValidator(models.Model):
    code = models.CharField(max_length=256, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Alumno (models.Model):
    legajo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s - Legajo:%i" %(self.nombre,self.apellido,self.legajo)