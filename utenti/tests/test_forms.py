import datetime

from django.test import TestCase
from utenti.forms import UserForm, UtenteCineDateForm


class TestForms(TestCase):

    def test_user_form_valid_data(self):
        form = UserForm(data={
            'username': 'mariorossi',
            'first_name': 'Mario',
            'last_name': 'Rossi',
            'email': 'mario.rossi@gmail.com',
            'password': 'pass123',
            'conferma_password': 'pass123'
        }, oauth_user=0)

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = UserForm(data={}, oauth_user=0)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_utente_form_valid_data(self):
        form = UtenteCineDateForm(data={
            'indirizzo': 'Via Vivarelli 17',
            'citta': 'Modena',
            'provincia': 'MO',
            'regione': 'Emilia-Romagna',
            'telefono': 3406370503,
            'sesso': 'Uomo',
            'data_nascita':  datetime.datetime.strptime('22/03/1996','%d/%m/%Y'),
            'generi_preferiti': ['Avventura','Horror'],
            'guidatore': True,
            'posti_macchina': 4
        })
        self.assertTrue(form.is_valid())

    def test_utente_form_no_data(self):
        form = UtenteCineDateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 9)