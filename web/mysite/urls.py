"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.staticfiles.views import serve
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from alumno.views import LoginView, SignupEmailSentView, SignupNotVerified, SignupVerified, SignupVerifyView, SignupView,LogoutView
admin.autodiscover()

urlpatterns = [
    path('jet/', include('jet.urls'), name='jet'),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('stock/', include("stock.urls")),
    path('turno/', include("turno.urls")),
    path('pago/', include("pago.urls")),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT,'show_indexes':settings.DEBUG}),
    url(r'^logout/$', LogoutView.as_view(), name="logout_page"),
    url(r'^signup/$', SignupView.as_view(), name='signup_page'),
    url(r'^signup/email_sent/$', SignupEmailSentView.as_view(), name='signup_email_sent_page'),
    url(r'^signup/verify/yes/$', SignupVerified.as_view(), name='signup_verified_page'),
    url(r'^signup/verify/not/$', SignupNotVerified.as_view(), name='signup_not_verified_page'),
    url(r'^signup/verify/$', SignupVerifyView.as_view(), name='signup_verify'),
    url(r'^password/reset/$', PasswordResetView.as_view(),{'template_name':'home_password_reset.html',
                                          'email_template_name':'email/home_reset_password.txt',
                                          'html_email_template_name':'email/home_reset_password.html',
                                          'subject_template_name':'email/home_reset_password_subject.txt',
                                          'password_reset_form': PasswordResetForm,
                                          'from_email': settings.EMAIL_HOST_USER,
                                          }, name='password_reset_page'),
    url(r'^password/reset/done/$', PasswordResetDoneView.as_view(),{'template_name':'home_password_reset_email_sent.html'},name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
    {'template_name': 'home_password_reset_verified.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', PasswordResetCompleteView.as_view(), {'template_name': 'home_password_reset_success.html'},
    name='password_reset_complete'),
    url(r'^$', LoginView, name='login_page'),

]
