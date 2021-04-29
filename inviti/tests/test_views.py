from django.test import TestCase, Client
from django.urls import reverse
from inviti.models import Invito
from utenti.models import Profile, User
import datetime
from django.utils import timezone
import pytest


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.user_unauthenticated = Client()
        self.user_login = Client()
        self.user_login2 = Client()

        self.user = User.objects.create_user(username='normale', password='12345')
        self.profilo = Profile.objects.get(user=self.user)
        self.user_login.login(username='normale', password='12345')

        self.user2 = User.objects.create_user(username='normale2', password='12345')
        self.profilo2 = Profile.objects.get(user=self.user2)
        self.user_login2.login(username='normale2', password='12345')

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

        self.invito = Invito.objects.create(
            tipologia='Netflix',
            cinema='',
            film='Titolo Film',
            data=datetime.datetime.strptime('25/06/2021', '%d/%m/%Y'),
            orario=datetime.datetime.strptime('21:00', '%H:%M'),
            limite_persone=4,
            genere=['Azione', 'Horror'],
            utente=self.user,
            commento='',
            data_invito=timezone.now(),
        )
        self.invito.partecipanti.add(self.user_oauth)
        self.invito.save()

    # HomeView
    def test_home_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('inviti-home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/home.html')

    def test_home_authenticated(self):
        response = self.user_login.get(reverse('inviti-home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/home.html')

    def test_home_oauth(self):
        response = self.user_oauth_login.get(reverse('inviti-home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/home.html')

    # InvitoDetailView
    def test_detail_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('invito-detail', args=[self.invito.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_detail.html')

    def test_detail_authenticated(self):
        response = self.user_login.get(reverse('invito-detail', kwargs={'pk': self.invito.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_detail.html')

    def test_detail_oauth(self):
        response = self.user_login.get(reverse('invito-detail', kwargs={'pk': self.invito.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_detail.html')

    # InvitoCreateView
    def test_create_invito_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('invito-create'))
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_create_invito_authenticated(self):
        response = self.user_login.get(reverse('invito-create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_form.html')

    def test_create_invito_oauth(self):
        response = self.user_oauth_login.get(reverse('invito-create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_form.html')

    # InvitoUpdateView
    def test_update_invito_unauthenticated(self):
        url = reverse('invito-update', kwargs={'pk': self.invito.id})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_update_invito_authenticated_creator(self):
        url = reverse('invito-update', kwargs={'pk': self.invito.id})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_form.html')

    def test_update_invito_authenticated_error_user(self):
        url = reverse('invito-update', kwargs={'pk': self.invito.id})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 403)

    # InvitoDeleteView
    def test_delete_invito_unauthenticated(self):
        url = reverse('invito-delete', kwargs={'pk': self.invito.id})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_delete_invito_authenticated_creator(self):
        url = reverse('invito-delete', kwargs={'pk': self.invito.id})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/invito_confirm_delete.html')

    def test_delete_invito_authenticated_error_user(self):
        url = reverse('invito-delete', kwargs={'pk': self.invito.id})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 403)

    # InvitiUtente
    def test_inviti_utente_unauthenticated(self):
        url = reverse('inviti-utente', kwargs={'username': 'normale'})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_utente.html')

    def test_inviti_utente_authenticated(self):
        url = reverse('inviti-utente', kwargs={'username': 'normale'})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_utente.html')

    def test_inviti_utente_oauth(self):
        url = reverse('inviti-utente', kwargs={'username': 'normale'})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_utente.html')

    def test_inviti_utente_unauthenticated_error_username(self):
        url = reverse('inviti-utente', kwargs={'username': 'wrong_username'})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 404)

    # PrenotazioniUtente
    def test_prenotazioni_utente_unauthenticated(self):
        url = reverse('prenotazioni-utente', kwargs={'username': 'normale'})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_prenotazioni_utente_authenticated(self):
        url = reverse('prenotazioni-utente', kwargs={'username': 'normale'})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/prenotazioni_utente.html')

    def test_prenotazioni_utente_authenticated_error_user(self):
        url = reverse('prenotazioni-utente', kwargs={'username': 'normale'})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 403)

    # InvitiGenere
    def test_inviti_genere_unauthenticated(self):
        url = reverse('inviti-genere', kwargs={'genere': 'Azione'})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_genere.html')

    def test_inviti_genere_authenticated(self):
        url = reverse('inviti-genere', kwargs={'genere': 'Azione'})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_genere.html')

    def test_inviti_genere_oauth(self):
        url = reverse('inviti-genere', kwargs={'genere': 'Azione'})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_genere.html')

    def test_inviti_genere_error_genere(self):
        url = reverse('inviti-genere', kwargs={'genere': 'wrong_genere'})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 404)

    # InvitiFilterView
    def test_filter_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('inviti-filter'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_filter.html')

    def test_filter_authenticated(self):
        response = self.user_login.get(reverse('inviti-filter'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/inviti_filter.html')

    # GeneriView
    def test_generi_filter_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('generi-filter'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/generi_filter.html')

    def test_generi_filter_authenticated(self):
        response = self.user_login.get(reverse('generi-filter'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/generi_filter.html')

    # Partecipa
    def test_partecipa_invito_unauthenticated(self):
        url = reverse('invito-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_partecipa_invito_authenticated_creator(self):
        url = reverse('invito-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 403)

    def test_partecipa_invito_authenticated_user_valid(self):
        url = reverse('invito-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_login2.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/partecipa.html')

    def test_partecipa_invito_authenticated_user_not_valid(self):
        url = reverse('invito-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 403)

    # RimuoviPartecipa
    def test_rimuovi_partecipa_invito_unauthenticated(self):
        url = reverse('invito-rimuouvi-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_unauthenticated.get(url)
        self.assertEquals(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_rimuovi_partecipa_invito_authenticated_creator(self):
        url = reverse('invito-rimuouvi-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_login.get(url)
        self.assertEquals(response.status_code, 403)

    def test_rimuovi_partecipa_invito_authenticated_user_valid(self):
        url = reverse('invito-rimuouvi-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_oauth_login.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inviti/rimuovi_partecipazione.html')

    def test_rimuovi_partecipa_invito_authenticated_user_not_valid(self):
        url = reverse('invito-rimuouvi-partecipa', kwargs={'pk': self.invito.id})
        response = self.user_login2.get(url)
        self.assertEquals(response.status_code, 403)

