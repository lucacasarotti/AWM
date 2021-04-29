from django.test import TestCase
from inviti.forms import InvitoForm
from utenti.models import User
from django.utils import timezone


class TestForms(TestCase):

    def test_invito_form_valid_data(self):
        user = User.objects.create_user(username='normale', password='12345')

        form = InvitoForm(data={
            'tipologia': 'Netflix',
            'film': 'Titolo Film',
            'data': '25/06/2021',
            'orario': '21:00',
            'limite_persone': 4,
            'genere': ['Azione', 'Horror'],
            'utente': user,
            'data_invito': timezone.now()
        })

        self.assertTrue(form.is_valid())

    def test_invito_form_no_data(self):
        form = InvitoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)




