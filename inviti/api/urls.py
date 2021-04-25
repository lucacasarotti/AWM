from inviti.api.views import InvitiListView, InvitoCreateView, InvitoDetailUpdateDelete, PartecipaInvito, CercaFilm, InvitiUtenteListView, PrenotazioniListView, ProvaInvitiListView
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'inviti'

urlpatterns = [
    path('list/', InvitiListView.as_view(), name="api-list-view"),
    path('prova/', ProvaInvitiListView.as_view(), name="api-list-view"),
    path('create/', InvitoCreateView.as_view(), name="api-create-view"),
    path('detail/<pk>/', InvitoDetailUpdateDelete.as_view(), name="api-detail-view"),
    path('partecipa/<pk>/', PartecipaInvito.as_view(), name="api-partecipa-view"),
    path('cerca/<str:titolo>/', CercaFilm.as_view(), name='api-cerca-film'),

    path('utente/<str:username>/', InvitiUtenteListView.as_view(), name='api-inviti-utente'),
    path('prenotazioni/<str:username>/', PrenotazioniListView.as_view(), name='api-prenotazioni-utente'),

    path('test/token/', obtain_auth_token, name='obtain-token'),
    path('test/api-auth/', include('rest_framework.urls')),
    path('test/rest-auth/', include('rest_auth.urls')),
]
