from django.conf.urls import url
from django.urls import path

from .views import *

app_name = 'API'

urlpatterns = [

    # prende le informazioni di un utente
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET
    path('utenti/profilo/<int:pk>/', userInfoLogin.as_view(), name='API-user-info'),

    # prende le informazioni dell'utente che ha richiamato l'api e ne permette la modifica
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET / PUT - serve essere loggati
    path('utenti/profilo/', selfUserInfoLogin.as_view(), name='API-self-user-info'),


    # completa la registrazione per un utente normale
    # /API/utenti/registra/utente-normale metodi ammessi :PUT
    path('utenti/registra/utente/', completaRegUtente.as_view(),
        name='API-registra-utente'),

    # cerca l'utente per username
    # /API/utenti/cerca/<char:name>' GET : tutti gli utenti
    path('utenti/cerca/<str:name>/', cercaUtente.as_view(), name='API-cerca-utente'),
    path('utenti/check_username/',check_username),
    # recensisci utenti
    # recensioni/nuova/<utente_recensito>/ metodi ammessi  POST : a tutti gli utenti
    # in automatico verrà settato il nickname di chi scrive la recensione
    path('recensioni/nuova/<str:utente>/',
        recensisciUtente.as_view(),
        name='API-recensisci-utenti'),

    # recensioni di un utente
    # /API/recensioni/ricevute/<utente>/  metodi ammessi  GET : a tutti gli utenti
    path('recensioni/ricevute/<str:utente>/',
        recensioniRicevute.as_view(),
        name='API-lista-recensioni-utente'),

    path('chat/',RoomModelViewSet.as_view(),name='get-rooms'),
    path('chat/<int:room_name>/messages/', MessageModelViewSet.as_view(),
         name='get-messages'),
    path('chat/<int:room_name>/messages/<int:id>/', RetrieveMessageViewSet.as_view(),
         name='get-new_message'),
]