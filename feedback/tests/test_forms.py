from django.test import TestCase
from feedback.forms import FeedbackForm


class TestForms(TestCase):

    def test_feedback_form_valid_data(self):
        form = FeedbackForm(data={
            'titolo': 'Recensione',
            'descrizione': 'Una descrizione',
            'voto': 5
        })

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = FeedbackForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
