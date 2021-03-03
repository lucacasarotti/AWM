from django.conf.urls import url
from django.urls import path

from . import views

app_name='utenti'

urlpatterns = [



    # /utenti/registrazione/
    path('registrazione/', views.registrazione, name='registrazione'),

]