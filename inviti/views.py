from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from chatroom.models import Room
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Invito
from .forms import InvitoForm
from static import GeoList, GenreList, CinemaList, TipologiaList
from django import forms
import functools
import operator
from django.db.models import Q, Case, When, Value, IntegerField
from django_filters.views import FilterView
from .filters import InvitoFilter, InvitoFilterFormHelper
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from inviti.api.serializers import InvitoSerializer
from datetime import datetime
from itertools import chain
from math import sin, cos, sqrt, atan2, radians
from utenti.views import calcola_lat_lon
from utenti.models import Profile


def ordina_inviti(user_profile, inviti):
    """
    Ordina gli annunci per distanza geografica secondo la selezione fatta dall'utente.
    :param user_profile: profilo utente.
    :param annunci_validi: lista degli annunci che verranno mostrati.
    :param ordina: indica se l'ordinamento deve essere crescente, decrescente o non ordinare.
    :return: indici degli annunci ordinati.
    """
    lat_user = 0
    lng_user = 0
    if user_profile.latitudine is not None and user_profile.longitudine is not None:
        lat_user = user_profile.latitudine
        lng_user = user_profile.longitudine
    distanze = []
    indici = []

    res = []

    # raggio della terra approssimato, in km
    r = 6373.0

    lat1 = radians(lat_user)
    lon1 = radians(lng_user)

    # Calcola le distanze di tutti gli annunci
    for i, annuncio in enumerate(inviti):
        indici.append(i)
        annuncio_profilo = Profile.objects.get(pk=annuncio.utente.id)

        if annuncio_profilo.latitudine is not None and annuncio_profilo.longitudine is not None:
            lat2 = radians(annuncio_profilo.latitudine)
            lon2 = radians(annuncio_profilo.longitudine)
        else:
            lat2 = 0
            lon2 = 0

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        d = r * c
        distanze.append(d)

    distanze, indici = (list(t) for t in zip(*sorted(zip(distanze, indici))))

    inviti_ordinati = []
    for i in indici:
        inviti_ordinati.append(inviti[i].id)

    print(inviti_ordinati)
    '''
    indici = get_vicini(p, queryset)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(indici)])
    qs = Invito.objects.filter(pk__in=indici).order_by(preserved)
    '''

    return inviti_ordinati

def create_queryset(dict):
    query_string = ''
    for key in dict:
        if dict[key] == 'true' and key not in ['last_mod', 'page_no', 'type', 'csrfmiddlewaretoken']:
            query_string = key + ' ' + query_string
    query_string = query_string[:-1]

    argument_list = []
    fields = ['genere']

    for query in query_string.split(' '):
        for field in fields:
            argument_list.append(Q(**{field + '__icontains': query}))

    query_set = Invito.objects.filter(functools.reduce(operator.or_, argument_list)).order_by('data')
    return query_set


class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 10

    def paginate(self, object_list, page=1, limit=10, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        data = {
            'pages': paginator.num_pages,
            'previous_page': objects.has_previous() and objects.previous_page_number() or None,
            'next_page': objects.has_next() and objects.next_page_number() or None,
            'data': list(objects),
        }
        return data


def about(request):
    profile = Profile.objects.get(pk=5)
    lat=0
    long=0
    lat, long = calcola_lat_lon(request, profile)
    print(profile)
    print(lat)
    print(long)

    return render(request, 'inviti/about.html', {'title': 'About'})


# ---------------    LIST VIEWS    ---------------

def home(request):
    context = {
        'inviti': Invito.objects.all()
    }
    return render(request, 'inviti/home.html', context)


'''class InvitoListView(ListView):
    model = Invito
    template_name = 'inviti/home.html'
    context_object_name = 'inviti'
    ordering = ['-data_invito']
    paginate_by = 5'''


class InvitiHome(ViewPaginatorMixin, View):
    '''
    Classe di Homepage, visualizza tutti gli inviti futuri
    '''

    def get(self, request):
        inviti = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=10)
        # print(resources)
        context = {'inviti': resources['data'], 'num_pages': resources['pages']}

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=10)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/home.html', context=context)


class InvitiUtente(ViewPaginatorMixin, View):
    '''
    Classe per visualizzare tutti gli inviti di un utente, ordinati per data.
    Sono compresi anche quelli scaduti, in rosso, in coda
    '''

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        i = Q(utente=user, data__gte=datetime.today())
        s = Q(utente=user, data__lt=datetime.today())
        inviti = (Invito.objects.filter(i | s).annotate(
            search_type_ordering=Case(When(i, then=Value(1)), When(s, then=Value(0)), default=Value(-1),
                                      output_field=IntegerField(), )).order_by('-search_type_ordering', 'data'))
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=5)
        context = {
            'inviti': resources['data'],
            'num_pages': resources['pages'],
            'results_count': inviti.count(),
            'username': user.username,
        }

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=5)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/inviti_utente.html', context=context)


'''class UtenteInvitiListView(ListView):

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Invito.objects.filter(utente=user).order_by('data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inviti_utente'] = True
        return context'''


class PrenotazioniUtente(LoginRequiredMixin, UserPassesTestMixin, ViewPaginatorMixin, View):
    '''
    Classe per visualizzare tutte le prenotazioni di un utente dalle più vicine.
    Sono visualizzati anche quelle scadute, in coda, in rosso
    '''

    def get(self, request, *args, **kwargs):
        # inviti = Invito.objects.filter(Q(partecipanti__username=self.kwargs.get('username'))).order_by('data')
        i = Q(partecipanti__username=self.kwargs.get('username'), data__gte=datetime.today())
        s = Q(partecipanti__username=self.kwargs.get('username'), data__lt=datetime.today())
        inviti = (Invito.objects.filter(i | s).annotate(
            search_type_ordering=Case(When(i, then=Value(1)), When(s, then=Value(0)), default=Value(-1),
                                      output_field=IntegerField(), )).order_by('-search_type_ordering', 'data'))
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=5)
        context = {
            'inviti': resources['data'],
            'num_pages': resources['pages'],
            'results_count': inviti.count(),
            'username': self.kwargs.get('username'),
        }

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=5)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/prenotazioni_utente.html', context=context)

    def test_func(self):
        user_prenotazioni = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user == user_prenotazioni:
            return True
        return False


'''class UtentePrenotazioniListView2(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Invito
    template_name = 'inviti/inviti_utente.html'
    context_object_name = 'inviti'
    paginate_by = 5

    def get_queryset(self):
        return Invito.objects.filter(Q(partecipanti__username=self.kwargs.get('username'))).order_by('data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inviti_utente'] = False
        return context

    def test_func(self):
        user_prenotazioni = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user == user_prenotazioni:
            return True
        return False'''


class InvitiGenere(ViewPaginatorMixin, View):
    '''
    Visualizza tutti gli inviti (futuri) del genere specificato nell'url
    '''

    def get(self, request, *args, **kwargs):
        inviti = Invito.objects.filter(Q(genere__contains=self.kwargs.get('genere')),
                                       data__gte=datetime.today()).order_by('data')
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=5)
        context = {
            'inviti': resources['data'],
            'num_pages': resources['pages'],
            'results_count': inviti.count(),
            'genere': self.kwargs.get('genere'),
        }

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=5)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/inviti_genere.html', context=context)


# ---------------    FILTER VIEWS    ---------------

class InvitiFilterView(FilterView):
    template_name = 'inviti/inviti_filter.html'

    filterset_class = InvitoFilter
    formhelper_class = InvitoFilterFormHelper
    paginate_by = 5
    context_object_name = 'inviti'
    ordering = ['data']

    def get_queryset(self):
        queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset


class GeneriFilterView(ViewPaginatorMixin, View):

    def get(self, request):
        if request.is_ajax():
            inviti = create_queryset(request.GET)
            serialized = InvitoSerializer(inviti, many=True)
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=10)
            return JsonResponse({"resources": resources})

        inviti = Invito.objects.all().order_by('data')
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=10)
        context = {'inviti': resources['data'],
                   'num_pages': resources['pages'],
                   'generi_list': GenreList.GenreList.generi_value_list,
                   'tipologie_list': TipologiaList.TipologiaList.tipologia_value_list
                   }
        return render(request, 'inviti/generi_filter.html', context=context)


# ---------------    DETAIL VIEWS    ---------------

class InvitoDetailView(DetailView):
    model = Invito
    context_object_name = 'invito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invito = self.get_object()
        if invito.posti_rimasti != invito.limite_persone:
            context['partecipanti_attuali'] = invito.partecipanti.all()

        room = Room.objects.filter(invito=invito)
        if room:
            context['room'] = room[0]
            context['users_room'] = room[0].users.all()

        return context


# ---------------    CREATE VIEWS    ---------------

class InvitoCreateView(LoginRequiredMixin, CreateView):
    model = Invito
    form_class = InvitoForm

    def form_valid(self, form):
        form.instance.utente = self.request.user
        response = super().form_valid(form)
        room = Room(title=form.instance.film, invito=self.object)
        room.save()
        room.users.add(self.request.user)
        room.save()
        return response


# ---------------    UPDATE VIEWS    ---------------

class InvitoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invito
    form_class = InvitoForm

    def form_valid(self, form):
        form.instance.utente = self.request.user
        return super().form_valid(form)

    def test_func(self):
        invito = self.get_object()
        if self.request.user == invito.utente:
            return True
        return False


class InvitoPartecipa(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invito
    template_name = 'inviti/partecipa.html'
    fields = []

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        utente = self.request.user
        invito = self.get_object()
        invito.partecipanti.add(utente.id)
        invito.save()
        room = Room.objects.filter(invito=invito)
        if room:
            room = room[0]
            room.users.add(utente)
            room.save()
        return redirect_url

    def test_func(self):
        invito = self.get_object()
        if self.request.user != invito.utente and invito.posti_rimasti > 0 and self.request.user not in invito.partecipanti.all():
            return True
        return False


class InvitoRimuoviPartecipa(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invito
    template_name = 'inviti/rimuovi_partecipazione.html'
    fields = []

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        utente = self.request.user
        invito = self.get_object()
        invito.partecipanti.remove(utente.id)
        invito.save()
        room = Room.objects.filter(invito=invito)
        if room:
            room = room[0]
            room.users.remove(utente)
            room.save()
        return redirect_url

    def test_func(self):
        invito = self.get_object()
        if self.request.user != invito.utente and self.request.user in invito.partecipanti.all():
            return True
        return False


# ---------------    DELETE VIEWS    ---------------

class InvitoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invito
    context_object_name = 'invito'
    success_url = '/inviti/'

    def test_func(self):
        invito = self.get_object()
        if self.request.user == invito.utente:
            return True
        return False
