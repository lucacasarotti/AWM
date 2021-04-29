from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inviti.views import (
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


class TestUrls(SimpleTestCase):

    # path('', InvitiHome.as_view(), name='inviti-home'),
    def test_list_url_resolves(self):
        url = reverse('inviti-home')
        self.assertEquals(resolve(url).func.view_class, InvitiHome)

    # path('nuovo/', InvitoCreateView.as_view(), name='invito-create'),
    def test_nuovo_url_resolves(self):
        url = reverse('invito-create')
        self.assertEquals(resolve(url).func.view_class, InvitoCreateView)

    # path('filtra/', InvitiFilterView.as_view(), name='inviti-filter'),
    def test_filtra_url_resolves(self):
        url = reverse('inviti-filter')
        self.assertEquals(resolve(url).func.view_class, InvitiFilterView)

    # path('about/', About.as_view(), name='inviti-about'),
    def test_about_url_resolves(self):
        url = reverse('inviti-about')
        self.assertEquals(resolve(url).func.view_class, About)

    # path('invito/<int:pk>/', InvitoDetailView.as_view(), name='invito-detail'),
    def test_detail_url_resolves(self):
        url = reverse('invito-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, InvitoDetailView)

    # path('invito/<int:pk>/partecipa/', InvitoPartecipa.as_view(), name='invito-partecipa'),
    def test_partecipa_url_resolves(self):
        url = reverse('invito-partecipa', args=[1])
        self.assertEquals(resolve(url).func.view_class, InvitoPartecipa)

    # path('invito/<int:pk>/rimuovi_partecipa/', InvitoRimuoviPartecipa.as_view(), name='invito-rimuouvi-partecipa'),
    def test_rimuovi_partecipa_url_resolves(self):
        url = reverse('invito-rimuouvi-partecipa', args=[1])
        self.assertEquals(resolve(url).func.view_class, InvitoRimuoviPartecipa)

    # path('invito/<int:pk>/update/', InvitoUpdateView.as_view(), name='invito-update'),
    def test_update_url_resolves(self):
        url = reverse('invito-update', args=[1])
        self.assertEquals(resolve(url).func.view_class, InvitoUpdateView)

    # path('invito/<int:pk>/delete/', InvitoDeleteView.as_view(), name='invito-delete'),
    def test_delete_url_resolves(self):
        url = reverse('invito-delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, InvitoDeleteView)

    # path('utente/<str:username>', InvitiUtente.as_view(), name='inviti-utente'),
    def test_inviti_utente_url_resolves(self):
        url = reverse('inviti-utente', args=['some-username'])
        self.assertEquals(resolve(url).func.view_class, InvitiUtente)

    # path('utente/<str:username>/prenotazioni', PrenotazioniUtente.as_view(), name='prenotazioni-utente'),
    def test_prenotazioni_utente_url_resolves(self):
        url = reverse('prenotazioni-utente', args=['some-username'])
        self.assertEquals(resolve(url).func.view_class, PrenotazioniUtente)

    # path('generi/', GeneriFilterView.as_view(), name='generi-filter'),
    def test_filtro_generi_url_resolves(self):
        url = reverse('generi-filter')
        self.assertEquals(resolve(url).func.view_class, GeneriFilterView)

    # path('genere/<str:genere>', InvitiGenere.as_view(), name='inviti-genere'),
    def test_inviti_genere_url_resolves(self):
        url = reverse('inviti-genere', args=['some-genere'])
        self.assertEquals(resolve(url).func.view_class, InvitiGenere)
