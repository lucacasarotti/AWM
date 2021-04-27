import datetime

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from utenti.models import Profile
import pytest

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from utenti.models import Profile
import pytest


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.user_unauthenticated = Client()
        self.user_login = Client()
        self.user = User.objects.create_user(username='normale', password='12345')

        self.profilo = Profile.objects.get(user=self.user)
        # profilo.user = self.user_normale,
        self.profilo.indirizzo = 'Via Vivarelli 17'
        self.profilo.citta = 'Modena'
        self.profilo.provincia = 'Modena'
        self.profilo.regione = 'Emilia Romagna'
        self.profilo.latitudine = 0
        self.profilo.longitudine = 0
        self.profilo.telefono = 3406370503
        self.profilo.sesso = 'Uomo'
        self.profilo.foto_profilo = None
        self.profilo.data_nascita = datetime.datetime.strptime('22/03/1996', '%d/%m/%Y')
        self.profilo.generi_preferiti= ['Avventura', 'Horror'],
        self.profilo.guidatore=True
        self.profilo.posti_macchina=4
        self.profilo.save()

        self.user_login.login(username='normale', password='12345')

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

    def test_edit_profile_authenticated(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 1})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_authenticated_errato(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 10})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 404)

    def test_edit_profile_unauthenticated(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login' in response.url

    def test_logout_user_unauthenticated(self):
        path = reverse('utenti:logout_user')
        response = self.user_unauthenticated.get(path)
        assert 'utenti/login' in response.url

    def test_logout_user_authenticated(self):
        path = reverse('utenti:logout_user')
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_check_username_presente_unauthenticated(self):
        path = reverse('utenti:check_username')
        response = self.user_unauthenticated.get(path, {'username': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_check_username_presente_authenticated(self):
        path = reverse('utenti:check_username')
        response = self.user_login.get(path, {'username': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_elimina_profilo_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_elimina_profilo_authenticated_errato(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 10})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 404)

    def test_elimina_profilo_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login' in response.url

    def test_elimina_profilo_conferma_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_elimina_profilo_conferma_authenticated_errato(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 10})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 404)

    def test_elimina_profilo_conferma_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_login_user_unauthenticated(self):
        path = reverse('utenti:utenti_login')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/login.html')

    def test_login_user_authenticated(self):
        path = reverse('utenti:utenti_login')
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_oauth_unauthenticated(self):
        path = reverse('utenti:oauth_utente')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_oauth_authenticated(self):
        path = reverse('utenti:oauth_utente')
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_unauthenticated(self):
        path = reverse('utenti:registrazione')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/registrazione.html')

    def test_registrazione_authenticated_normale(self):
        path = reverse('utenti:registrazione')
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_view_profile_authenticated(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 1})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_unauthenticated(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_authenticated_errato(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 10})
        response = self.user_login.get(path)
        self.assertEqual(response.status_code, 404)

    def test_view_profile_unauthenticated_errato(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 10})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 404)

    def test_check_username_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:check_username'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_edit_profile_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:edit_profile', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_elimina_profilo_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:elimina_profilo', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_elimina_profilo_conferma_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_login_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:utenti_login'))
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_logout_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:logout_user'))
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:registrazione'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url

    def test_view_profilo_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:view_profile', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_utente/' in response.url


