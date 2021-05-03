from django.urls import path
from .views import (
    InvitiHome,
    InvitoDetailView,
    InvitoCreateView,
    InvitoUpdateView,
    InvitoDeleteView,
    InvitiUtente,
    PrenotazioniUtente,
    InvitoPartecipa,
    InvitiGenere,
    InvitoRimuoviPartecipa,
    InvitiFilterView,
    GeneriFilterView,
    About
)

#app_name = 'inviti'
urlpatterns = [
    # /inviti/
    path('', InvitiHome.as_view(), name='inviti-home'),
    # /inviti/nuovo
    path('nuovo/', InvitoCreateView.as_view(), name='invito-create'),
    # /inviti/filtra
    path('filtra/', InvitiFilterView.as_view(), name='inviti-filter'),
    # /inviti/about/
    path('about/', About.as_view(), name='inviti-about'),

    # /inviti/invito/<id_invito>
    path('invito/<int:pk>/', InvitoDetailView.as_view(), name='invito-detail'),
    # /inviti/invito/<id_invito>/partecipa
    path('invito/<int:pk>/partecipa/', InvitoPartecipa.as_view(), name='invito-partecipa'),
    # /inviti/invito/<id_invito>/rimuovi_partecipa
    path('invito/<int:pk>/rimuovi_partecipa/', InvitoRimuoviPartecipa.as_view(), name='invito-rimuouvi-partecipa'),
    # /inviti/invito/<id_invito>/update
    path('invito/<int:pk>/update/', InvitoUpdateView.as_view(), name='invito-update'),
    # /inviti/invito/<id_invito>/delete
    path('invito/<int:pk>/delete/', InvitoDeleteView.as_view(), name='invito-delete'),

    # /inviti/utente/<username>
    path('utente/<str:username>', InvitiUtente.as_view(), name='inviti-utente'),
    # /inviti/utente/<username>/prenotazioni
    path('utente/<str:username>/prenotazioni', PrenotazioniUtente.as_view(), name='prenotazioni-utente'),

    # /inviti/generi
    path('generi/', GeneriFilterView.as_view(), name='generi-filter'),
    # /inviti/genere/<genere>
    path('genere/<str:genere>', InvitiGenere.as_view(), name='inviti-genere'),


]
