from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'API'

urlpatterns = [

    # prende le informazioni di un utente
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET
    path('utenti/profilo/<int:pk>/', views.userInfoLogin.as_view(), name='API-user-info'),

    # prende le informazioni dell'utente che ha richiamato l'api e ne permette la modifica
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET / PUT - serve essere loggati
    path('utenti/profilo/', views.selfUserInfoLogin.as_view(), name='API-self-user-info'),


    # completa la registrazione per un utente normale
    # /API/utenti/registra/utente-normale metodi ammessi :PUT
    path('utenti/registra/utente-normale', views.completaRegUtentenormale.as_view(),
        name='API-registra-utente-normale'),

    # cerca l'utente per username
    # /API/utenti/cerca/<char:name>' GET : tutti gli utenti
    path('utenti/cerca/<str:name>/', views.cercaUtente.as_view(), name='API-cerca-utente'),

    # recensisci utenti
    # recensioni/nuova/<utente_recensito>/ metodi ammessi  POST : a tutti gli utenti
    # in automatico verrà settato il nickname di chi scrive la recensione
    path('recensioni/nuova/<str:utente>/',
        views.recensisciUtente.as_view(),
        name='API-recensisci-utenti'),

    # recensioni di un utente
    # /API/recensioni/ricevute/<utente>/  metodi ammessi  GET : a tutti gli utenti
    path('recensioni/ricevute/<str:utente>/',
        views.recensioniRicevute.as_view(),
        name='API-lista-recensioni-utente'),
]