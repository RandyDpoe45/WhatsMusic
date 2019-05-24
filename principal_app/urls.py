from django.urls import path

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views as aux
from django.contrib.auth import views as auth_views
from django.urls import re_path
from . import views

urlpatterns =[


    url(r'^registro/$',views.serveRegistro, name = 'registro'),
    url(r'^crearRegistro/$',views.crearRegistro, name = 'crearRegistro'),
    url(r'^login/$',views.login, name = 'login'),
    url(r'^autenticar/$',views.auteticarIngreso, name = 'autenticar'),
    url(r'^bancoProyectos/$', views.serveBancoProyectos),
    url(r'^crearProyecto/$',views.crearProyecto),
    url(r'^borrarProyecto/$',views.borrarProyecto),
    url(r'^bancotrabajo/$',views.serveBancoTrabajo),
    url(r'^$',views.serveHome, name ='home')

]
#urlpatterns +=[re_path(r'^static/(?P<path>.*)$',aux.serve)]
