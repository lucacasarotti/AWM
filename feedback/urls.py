from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'recensioni'

urlpatterns = [

    # /recensioni/nuova/#user_recensito/
   # path('nuova/<int:oid>/', views.nuova_recensione, name='nuova_recensione'),

    # /recensioni/ricevute/@username/
    #path('ricevute/<int:oid>/', views.recensioni_ricevute, name='recensioni_ricevute'),
]