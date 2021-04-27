import datetime

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
        self.profilo.indirizzo='Via Vivarelli'
        self.profilo.citta='Modena'
        self.profilo.provincia='Modena'
        self.profilo.regione='Emilia Romagna'
        self.profilo.latitudine=0
        self.profilo.longitudine=0
        self.profilo.telefono=3391234567
        self.profilo.foto_profilo=None
        self.profilo.sesso='Uomo'
        self.profilo.generi_preferiti=['Avventura','Fantasy']
        self.profilo.data_nascita=datetime.datetime.strptime('22/03/1996','%d/%m/%Y')
        self.profilo.guidatore=True
        self.profilo.posti_macchina=4
        self.profilo.save()

        self.user_login.login(username='normale', password='12345')

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

    def test_nuovo_feedback(self):
        response = self.user_login.get(reverse('feedback:nuovo_feedback', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)


    def test_nuovo_feedback_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('feedback:nuovo_feedback', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login' in response.url

    def test_nuovo_feedback_errato(self):
        response = self.user_login.get(reverse('feedback:nuovo_feedback', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)

    def test_nuovo_feedback_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('feedback:nuovo_feedback', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login' in response.url

    def test_feedback_ricevuti_authenticated(self):
        path = reverse('feedback:get_feedback')
        response = self.user_login.get(path+'?user_recensito=1')
        self.assertEqual(response.status_code, 200)

    def test_feedback_ricevuti_authenticated_errato(self):
        path = reverse('feedback:get_feedback')
        response = self.user_login.get(path+'?user_recensito=10')
        self.assertEqual(response.status_code, 404)

    def test_feeback_ricevute_unauthenticated(self):
        path = reverse('feedback:get_feedback')
        response = self.user_unauthenticated.get(path+'?user_recensito=1')
        self.assertEqual(response.status_code, 200)

    def test_feeback_ricevute_unauthenticated_errato(self):
        path = reverse('feedback:get_feedback')
        response = self.user_unauthenticated.get(path+'?user_recensito=10')
        self.assertEqual(response.status_code, 404)
