from django import forms
from django.forms import ModelForm, Textarea
from static import CinemaList, GenreList
from .models import Invito
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re
from multiselectfield import MultiSelectField, MultiSelectFormField
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Fieldset, HTML, Row, Column, Submit,Field
from static import GeoList, GenreList, CinemaList, TipologiaList


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

# lookup_expr

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

    def __init__(self, *args, **kwargs):
        super(InvitoForm, self).__init__(*args, **kwargs)
        self.fields['tipologia'].widget.attrs.update({'id': 'tipo'})
        self.fields['tipologia'].label = 'Dove?'
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


class InvitoFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
            Row(
                Column('tipologia', css_class='form-group col-md-6 mb-0'),
                Column('film', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('data', css_class='form-group col-md-6 mb-0'),
                Column('orario', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineCheckboxes('genere'),
            Submit('submit', 'Cerca', css_class="btn btn-outline-info"),
        )