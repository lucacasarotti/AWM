from django.urls import path

from .views import *

app_name = 'API'

urlpatterns = [

    path('inviti/list/', InvitiListView.as_view(), name="api-list-view"),
    path('inviti/create/', InvitoCreateView.as_view(), name="api-create-view"),
    path('inviti/detail/<pk>/', InvitoDetailUpdateDelete.as_view(), name="api-detail-view"),
    path('inviti/partecipa/<pk>/', PartecipaInvito.as_view(), name="api-partecipa-view"),
    path('inviti/cerca/<str:titolo>/', CercaFilm.as_view(), name='api-cerca-film'),

    path('inviti/utente/<str:username>/', InvitiUtenteListView.as_view(), name='api-inviti-utente'),
    path('inviti/prenotazioni/<str:username>/', PrenotazioniListView.as_view(), name='api-prenotazioni-utente'),

    path('utenti/profilo/<int:pk>/', userInfoLogin.as_view(), name='API-user-info'),
    path('utenti/profilo/', selfUserInfoLogin.as_view(), name='API-self-user-info'),
    path('utenti/registra/utente/', completaRegUtente.as_view(), name='API-registra-utente'),
    path('utenti/cerca/<str:name>/', cercaUtente.as_view(), name='API-cerca-utente'),
    path('utenti/check_username/', check_username),

    path('recensioni/nuova/<str:utente>/', recensisciUtente.as_view(), name='API-recensisci-utenti'),
    path('recensioni/ricevute/<str:utente>/', recensioniRicevute.as_view(), name='API-lista-recensioni-utente'),

    path('chat/', RoomModelViewSet.as_view(),name='get-rooms'),
    path('chat/<int:room_name>/messages/', MessageModelViewSet.as_view(), name='get-messages'),
    path('chat/<int:room_name>/messages/<int:id>/', RetrieveMessageViewSet.as_view(), name='get-new_message'),
]
