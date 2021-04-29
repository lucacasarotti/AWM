import django_filters
from .forms import *
from static import GenreList, TipologiaList
from math import sin, cos, sqrt, atan2, radians
from utenti.models import Profile


def get_vicini(user_profile, inviti, distanza_massima = 40):
    '''
    Seleziona solo gli inviti vicini all'utente per distanza geografica < distanza_massima (in km).
    :param user_profile: profilo utente.
    :param inviti: queryset contenente gli inviti da filtrare.
    :param distanza_massima: indica la massima distanza per cui filtrare gli inviti.
    :return: queryset degli annunci vicini.
    '''
    lat_user = 0
    lng_user = 0
    if user_profile.latitudine is not None and user_profile.longitudine is not None:
        lat_user = user_profile.latitudine
        lng_user = user_profile.longitudine

    indici = []

    # raggio della terra approssimato, in km
    r = 6373.0

    lat1 = radians(lat_user)
    lon1 = radians(lng_user)

    # Calcola le distanze di tutti gli annunci
    for i, invito in enumerate(inviti):

        invito_profilo = Profile.objects.get(pk=invito.utente.id)

        if invito_profilo.latitudine is not None and invito_profilo.longitudine is not None:
            lat2 = radians(invito_profilo.latitudine)
            lon2 = radians(invito_profilo.longitudine)
        else:
            lat2 = 0
            lon2 = 0

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        d = r * c
        # print(d, invito.utente, invito_profilo.indirizzo)
        if d < distanza_massima:
            indici.append(invito.id)

    return inviti.filter(pk__in=indici)


class InvitoFilter(django_filters.FilterSet):
    tipologia = django_filters.MultipleChoiceFilter(widget=forms.CheckboxSelectMultiple,
                                                    choices=TipologiaList.TipologiaList.ListaTipologia)
    film = django_filters.CharFilter(lookup_expr='icontains')
    data = django_filters.DateFilter(widget=DateInput())
    orario = django_filters.TimeFilter(widget=TimeInput())
    genere = django_filters.MultipleChoiceFilter(widget=forms.CheckboxSelectMultiple,
                                                 choices=GenreList.GenreList.ListaGeneri, lookup_expr='icontains')
    vicini_a_me = django_filters.BooleanFilter(widget=forms.CheckboxInput, method='vicini')

    class Meta:
        model = Invito
        fields = ['tipologia', 'film', 'data', 'orario', 'genere', 'vicini_a_me']

    def __init__(self, *args, **kwargs):
        super(InvitoFilter, self).__init__(*args, **kwargs)
        self.filters['genere'].label = 'Generi'
        self.filters['tipologia'].label = 'Dove'
        self.filters['film'].label = 'Titolo del film'
        self.filters['vicini_a_me'].label = 'Solo inviti vicini a me'

    def vicini(self, queryset, name, value):
        '''
        Se l'utente è autenticato e il parametro è selezionato ritorna un
        queryset ristretto agli inviti nel raggio di 30 km
        '''
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and value:
            p = Profile.objects.get(pk=user.id)
            qs = get_vicini(p, queryset, 40)
            return qs
        return queryset


class InvitoFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
            InlineCheckboxes('tipologia'),
            'film',
            Row(
                Column('data', css_class='form-group col-md-6 mb-0'),
                Column('orario', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'vicini_a_me',
            InlineCheckboxes('genere'),
            Submit('submit', 'Cerca', css_class="btn btn-outline-info"),
        )


