import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from feedback.models import Recensione


class FeedbackForm(forms.ModelForm):
    required_css_class = 'required'
    descrizione = forms.CharField(widget=forms.Textarea)
    voto_select = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    voto = forms.ChoiceField(choices=voto_select)

    class Meta:
        model = Recensione
        fields = ['titolo', 'descrizione', 'voto']

    def clean_descrizione(self):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 ,.'èòàùì]+$", self.cleaned_data['descrizione']):
            raise ValidationError(_('Errore: la descrizione può contenere solo lettere, '
                                    'numeri, punti, virgole e spazi.'))
        return self.cleaned_data['descrizione']

    def clean_titolo(self):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", self.cleaned_data['titolo']):
            raise ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(self.cleaned_data['titolo']) <= 95):
            raise ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['titolo']
