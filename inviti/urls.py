from django.urls import path
from . import views
from .views import (
    InvitoListView,
    InvitoDetailView,
    InvitoCreateView,
    InvitoUpdateView,
    InvitoDeleteView,
    UtenteInvitiListView,
    UtentePrenotazioniListView,
    InvitoPartecipa,
    GenereInvitoListView,
    InvitoRimuoviPartecipa,
    InvitiFilterView
)

#app_name = 'inviti'
urlpatterns = [
    #path('', views.home, name='inviti-home'),
    # /inviti/
    path('', InvitoListView.as_view(), name='inviti-home'),
    # /inviti/utente/<username>
    path('utente/<str:username>', UtenteInvitiListView.as_view(), name='inviti-utente'),
    # /inviti/utente/<username>/prenotazioni
    path('utente/<str:username>/prenotazioni', UtentePrenotazioniListView.as_view(), name='prenotazioni-utente'),
    # /inviti/utente/<username>
    path('genere/<str:genere>', GenereInvitoListView.as_view(), name='inviti-genere'),
    # /inviti/invito/<id_invito>
    path('invito/<int:pk>/', InvitoDetailView.as_view(), name='invito-detail'),
    # /inviti/invito/<id_invito>/partecipa
    path('invito/<int:pk>/partecipa/', InvitoPartecipa.as_view(), name='invito-partecipa'),
    # /inviti/invito/<id_invito>/partecipa
    path('invito/<int:pk>/rimuovi_partecipa/', InvitoRimuoviPartecipa.as_view(), name='invito-rimuouvi-partecipa'),
    # /inviti/nuovo
    path('nuovo/', InvitoCreateView.as_view(), name='invito-create'),
    # /inviti/filtra
    path('filtra/', InvitiFilterView.as_view(), name='inviti-filter'),
    # /inviti/invito/<id_invito>/update
    path('invito/<int:pk>/update/', InvitoUpdateView.as_view(), name='invito-update'),
    # /inviti/invito/<id_invito>/delete
    path('invito/<int:pk>/delete/', InvitoDeleteView.as_view(), name='invito-delete'),
    # /inviti/about/
    path('about/', views.about, name='inviti-about'),
]
