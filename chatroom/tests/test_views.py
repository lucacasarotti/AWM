import datetime

from django.forms import TimeInput
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from utenti.models import Profile
from inviti.models import Invito
from chatroom.models import Room,MessageModel
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

        self.user_2_login = Client()
        self.user_2 = User.objects.create_user(username='secondo', password='12345')
        self.profilo2 = Profile.objects.get(user=self.user)
        self.profilo2.indirizzo = 'Via Vivarelli'
        self.profilo2.citta = 'Modena'
        self.profilo2.provincia = 'Modena'
        self.profilo2.regione = 'Emilia Romagna'
        self.profilo2.latitudine = 0
        self.profilo2.longitudine = 0
        self.profilo2.telefono = 3391234567
        self.profilo2.foto_profilo = None
        self.profilo2.sesso = 'Uomo'
        self.profilo2.generi_preferiti = ['Avventura', 'Fantasy']
        self.profilo2.data_nascita = datetime.datetime.strptime('22/03/1996', '%d/%m/%Y')
        self.profilo2.guidatore = True
        self.profilo2.posti_macchina = 4
        self.profilo2.save()

        self.user_2_login.login(username='secondo', password='12345')


        invito=Invito.objects.create(
            tipologia='Netflix',
            film='Test',
            data=datetime.datetime.strptime('06/05/2021','%d/%m/%Y'),
            orario='15:00',
            limite_persone=5,
            genere=['Horror','Fantasy'],
            commento="Spaziale",
            utente_id=1
        )

        self.Room=Room.objects.create(title="Test",invito=invito)
        self.Room.users.set([1,])
        self.Message=MessageModel(user=self.user,recipient=self.Room,body='test')

    def test_accedi_room(self):
        response = self.user_login.get(reverse('chatroom:chat', kwargs={'room_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_accedi_proibito(self):
        response = self.user_2_login.get(reverse('chatroom:chat', kwargs={'room_id': 1}))
        self.assertEqual(response.status_code, 403)

    def test_accedi_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('chatroom:chat', kwargs={'room_id': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login' in response.url

    def test_accedi_errato(self):
        response = self.user_login.get(reverse('chatroom:chat', kwargs={'room_id': 2}))
        self.assertEqual(response.status_code, 404)




    def test_get_list_messages(self):
        response = self.user_login.get(reverse('chatroom:get-messages', kwargs={'room_name': 1})+'?target=1')
        self.assertEqual(response.status_code, 200)

    def test_get_list_messages_proibito(self):
        response = self.user_2_login.get(reverse('chatroom:get-messages', kwargs={'room_name': 1}) + '?target=1')
        self.assertEqual(response.status_code, 403)

    def test_get_list_messages_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('chatroom:get-messages', kwargs={'room_name': 1}) + '?target=1')
        self.assertEqual(response.status_code, 403)

    def test_get_list_messages_errato(self):
        response = self.user_unauthenticated.get(
            reverse('chatroom:get-messages', kwargs={'room_name': 2}) + '?target=2')
        self.assertEqual(response.status_code, 404)

    def test_get_list_messages_errato_target(self):
        response = self.user_unauthenticated.get(
            reverse('chatroom:get-messages', kwargs={'room_name': 2}) + '?target=1')
        self.assertEqual(response.status_code, 403)



    def test_post_message(self):
        response = self.user_login.post(
            reverse('chatroom:get-messages', kwargs={'room_name': 1}),data={'recipient': 1,
        'body': 'message'})
        self.assertEqual(response.status_code, 201)

    def test_post_message_proibito(self):
        response = self.user_2_login.post(
            reverse('chatroom:get-messages', kwargs={'room_name': 1}),data={'recipient': 1,'body': 'message'})
        self.assertEqual(response.status_code, 403)

    def test_post_message_unauthenticated(self):
        response = self.user_unauthenticated.post(
            reverse('chatroom:get-messages', kwargs={'room_name': 1}),data={'recipient': 1,'body': 'message'})
        self.assertEqual(response.status_code, 403)

    def test_post_message_errato(self):
        response = self.user_login.post(
            reverse('chatroom:get-messages', kwargs={'room_name': 2}),data={'recipient': 2,'body': 'message'})
        self.assertEqual(response.status_code, 404)

    def test_post_message_errato_target(self):
        response = self.user_2_login.post(
            reverse('chatroom:get-messages', kwargs={'room_name': 2}),data={'recipient': 1,'body': 'message'})
        self.assertEqual(response.status_code, 403)








