import re
from datetime import datetime
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Invito


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class InvitoForm(forms.ModelForm):
    class Meta:
        model = Invito
        fields = ['tipologia', 'cinema', 'film', 'data', 'orario', 'limite_persone', 'genere', 'commento']
        widgets = {
            'film': forms.TextInput(attrs={'placeholder': 'Titolo del film'}),
            'cinema': forms.TextInput(attrs={'placeholder': 'Cinema (Città)'}),
            'commento': Textarea(attrs={'cols': 80, 'rows': 5}),
            'data': DateInput(),
            'orario': TimeInput(),
        }
        labels = {
            'tipologia': _('Dove?'),
        }

    def __init__(self, *args, **kwargs):
        super(InvitoForm, self).__init__(*args, **kwargs)
        self.fields['tipologia'].widget.attrs.update({'id': 'tipo'})
        self.fields['cinema'].widget.attrs.update({'id': 'selection_cinema'})
        self.fields['data'].widget.attrs.update({'id': 'datepicker'})
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('tipologia', css_class='form-group col-md-6 mb-0'),
                Column('cinema', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'film',
            Row(
                Column('data', css_class='form-group col-md-6 mb-0'),
                Column('orario', css_class='form-group col-md-4 mb-0'),
                Column('limite_persone', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            InlineCheckboxes('genere'),
            'commento',
            Submit('submit', 'Salva!', css_class="btn btn-outline-info"),

        )

    def clean_film(self):
        # controllo campo film
        if not re.match("^[A-Za-z0-9 .!,'èòàùì]+$", self.cleaned_data['film']):
            raise ValidationError(_('Errore: il campo film può contenere solo lettere, '
                                    'numeri, spazi e caratteri \"\'.!,\".'))
        if not (1 <= len(self.cleaned_data['film']) <= 95):
            raise ValidationError(_('Errore: il campo film deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['film']

    def clean_commento(self):
        # controllo campo commento
        if not (re.match("^[A-Za-z0-9 .!,'èòàùì]+$", self.cleaned_data['commento']) or self.cleaned_data['commento'] == ""):
            raise ValidationError(_('Errore: il campo commento può contenere solo lettere, '
                                    'numeri, spazi e caratteri \"\'.!,\".'))
        if not (len(self.cleaned_data['commento']) <= 245):
            raise ValidationError(_('Errore: il campo commento deve avere lunghezza fra 0 e 245 caratteri.'))
        return self.cleaned_data['commento']

    def clean_data(self):
        data = self.cleaned_data['data']
        if data < datetime.now().date():
            raise ValidationError(_('Viaggi nel tempo per caso?'))
        return self.cleaned_data['data']


class InvitoFormUpdate(forms.ModelForm):
    class Meta:
        model = Invito
        fields = ['tipologia', 'cinema', 'film', 'data', 'orario', 'genere', 'commento']
        widgets = {
            'film': forms.TextInput(attrs={'placeholder': 'Titolo del film'}),
            'cinema': forms.TextInput(attrs={'placeholder': 'Cinema (Città)'}),
            'commento': Textarea(attrs={'cols': 80, 'rows': 5}),
            'orario': TimeInput(),
        }
        labels = {
            'tipologia': _('Dove?'),
        }

    def __init__(self, *args, **kwargs):
        super(InvitoFormUpdate, self).__init__(*args, **kwargs)
        self.fields['tipologia'].widget.attrs.update({'id': 'tipo'})
        self.fields['cinema'].widget.attrs.update({'id': 'selection_cinema'})
        self.fields['data'].widget.attrs.update({'id': 'datepicker'})
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('tipologia', css_class='form-group col-md-6 mb-0'),
                Column('cinema', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'film',
            Row(
                Column('data', css_class='form-group col-md-6 mb-0'),
                Column('orario', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineCheckboxes('genere'),
            'commento',
            Submit('submit', 'Salva!', css_class="btn btn-outline-info"),

        )

    def clean_film(self):
        # controllo campo film
        if not re.match("^[A-Za-z0-9 .!,'èòàùì]+$", self.cleaned_data['film']):
            raise ValidationError(_('Errore: il campo film può contenere solo lettere, '
                                    'numeri, spazi e caratteri \"\'.!,\".'))
        if not (1 <= len(self.cleaned_data['film']) <= 95):
            raise ValidationError(_('Errore: il campo film deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['film']

    def clean_commento(self):
        # controllo campo commento
        if not (re.match("^[A-Za-z0-9 .!,'èòàùì]+$", self.cleaned_data['commento']) or self.cleaned_data['commento'] == ""):
            raise ValidationError(_('Errore: il campo commento può contenere solo lettere, '
                                    'numeri, spazi e caratteri \"\'.!,\".'))
        if not (len(self.cleaned_data['commento']) <= 245):
            raise ValidationError(_('Errore: il campo commento deve avere lunghezza fra 0 e 245 caratteri.'))
        return self.cleaned_data['commento']

    def clean_data(self):
        data = self.cleaned_data['data']
        if data < datetime.now().date():
            raise ValidationError(_('Viaggi nel tempo per caso?'))
        return self.cleaned_data['data']

