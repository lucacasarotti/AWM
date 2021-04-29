from django.test import TestCase, Client
from django.urls import reverse
from inviti.models import Invito
from utenti.models import Profile, User
import datetime
from django.utils import timezone


class TestModels(TestCase):
    def setUp(self):
        self.user_login = Client()
        self.user = User.objects.create_user(username='normale', password='12345')
        self.user_login.login(username='normale', password='12345')

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

    def test_posti_rimasti(self):
        self.invito.partecipanti.add(self.user_oauth)
        self.invito.save()
        self.assertEquals(self.invito.posti_rimasti, 3)

    def test_scaduto(self):
        self.invito.data = datetime.date.today() + datetime.timedelta(days=7)
        self.invito.save()
        self.assertEquals(self.invito.scaduto, False)
        self.invito.data = datetime.date.today() - datetime.timedelta(days=7)
        self.invito.save()
        self.assertEquals(self.invito.scaduto, True)


