import django_filters
from django import forms
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Fieldset, HTML, Row, Column, Submit,Field
from .models import *
from .forms import *
from static import GeoList, GenreList, CinemaList, TipologiaList


class InvitoFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(widget=DateInput())
    orario = django_filters.TimeFilter(widget=TimeInput())
    genere = django_filters.MultipleChoiceFilter(widget=forms.CheckboxSelectMultiple, choices=GenreList.GenreList.ListaGeneri,lookup_expr='icontains')

    class Meta:
        model = Invito
        fields = ['tipologia', 'film', 'data', 'orario', 'genere']

    '''def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('tipologia', 'Netflix')
        super().__init__(data, *args, **kwargs)'''
