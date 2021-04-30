import functools
import operator
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Case, When, Value, IntegerField
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from chatroom.models import Room
from utenti.models import Profile
from .models import Invito
from API.serializers import InvitoSerializer
from .forms import InvitoForm, InvitoFormUpdate
from static import GenreList, TipologiaList
from .filters import InvitoFilter, InvitoFilterFormHelper

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def create_queryset(dict):
    """
    Crea un queryset di inviti basato sui parametri true del dizionario passato
    :param dict: dizionario di parametri secondo cui filtrare gli inviti.
    :return: queryset con gli annunci filtrati.
    """
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

    query_set = Invito.objects.filter(functools.reduce(operator.or_, argument_list), data__gte=datetime.today()).order_by('data')

    return query_set


class ViewPaginatorMixin(object):
    """
    Classe di paginazione, crea un oggetto paginator e ritorna un dizionario contenente i risultati relativi
    alla pagina richiesta
    """
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


class About(ViewPaginatorMixin, View):
    '''
    Classe di Homepage, visualizza tutti gli inviti futuri
    '''

    def get(self, request):
        context = {}
        if request.user and request.user.is_authenticated:
            context = {'user_profile': Profile.objects.get(pk=request.user.id)}

        return render(request, 'inviti/about.html', context=context)


# ---------------    LIST VIEWS    ---------------

class InvitiHome(ViewPaginatorMixin, View):
    '''
    Classe di Homepage, visualizza tutti gli inviti futuri
    '''

    def get(self, request):
        if request.is_ajax():
            inviti = create_queryset(request.GET)
            serialized = InvitoSerializer(inviti, many=True)
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=10)
            return JsonResponse({"resources": resources})

        inviti = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=10)

        context = {'inviti': resources['data'], 'num_pages': resources['pages'], 'filtro_generi': True}
        if request.user and request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=request.user.id)

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

        if request.user and request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=request.user.id)

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=5)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/inviti_utente.html', context=context)


class PrenotazioniUtente(LoginRequiredMixin, UserPassesTestMixin, ViewPaginatorMixin, View):
    '''
    Classe per visualizzare tutte le prenotazioni di un utente a partire dalle più prossime.
    Sono visualizzate anche quelle scadute, in coda, in rosso
    '''
    login_url = '/utenti/login/'

    def get(self, request, *args, **kwargs):
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
            'user_profile': Profile.objects.get(pk=request.user.id)
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


class InvitiGenere(ViewPaginatorMixin, View):
    '''
    Visualizza tutti gli inviti (futuri) del genere specificato nell'url
    '''

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('genere') not in GenreList.GenreList.generi_value_list:
            raise Http404("Il genere cercato non esiste")
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

        if request.user and request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=request.user.id)

        if request.is_ajax():
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=5)
            return JsonResponse({"resources": resources})

        return render(request, 'inviti/inviti_genere.html', context=context)


# ---------------    FILTER VIEWS    ---------------

class InvitiFilterView(FilterView):
    '''
    Filtro avanzato sui campi 'tipologia', 'film', 'data', 'orario', 'genere'
    Se l'utente è autenticato è presente un ulteriore campo 'vicini_a_me' che ritorna gli inviti creati da utenti
    nel raggio di 40 km
    '''
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=self.request.user.id)
        return context


class GeneriFilterView(ViewPaginatorMixin, View):
    '''
    Filtro solo sui generi: all'attivazione di un filtro vengono mostrati tutti gli inviti relativi ad almeno un
    filtro selezionato (ordine per data)
    '''
    def get(self, request):
        if request.is_ajax():
            inviti = create_queryset(request.GET)
            serialized = InvitoSerializer(inviti, many=True)
            page_no = request.GET.get('page_no')
            resources = self.paginate(serialized.data, page=page_no, limit=10)
            return JsonResponse({"resources": resources})

        inviti = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
        serialized = InvitoSerializer(inviti, many=True)
        resources = self.paginate(serialized.data, limit=10)
        context = {'inviti': resources['data'],
                   'num_pages': resources['pages'],
                   'generi_list': GenreList.GenreList.generi_value_list,
                   'tipologie_list': TipologiaList.TipologiaList.tipologia_value_list
                   }
        if request.user and request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=request.user.id)
        return render(request, 'inviti/generi_filter.html', context=context)


# ---------------    DETAIL VIEWS    ---------------

class InvitoDetailView(DetailView):
    '''
    View di dettaglio dell'invito, visualizza tutte le informazioni di base sull'invito
    Se l'utente è autenticato ed è l'autore l'invito può  essere modificato o eliminato, se invece è autenticato ma
    non è l'autore allora vi è la possibilità di partecipare all'invito.
    Tutti i partecipanti, autore compreso, hanno quindi accesso da questa pagina alla chat.
    '''
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

        if self.request.user and self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=self.request.user.id)

        return context


# ---------------    CREATE VIEWS    ---------------

class InvitoCreateView(LoginRequiredMixin, CreateView):
    '''
    View di creazione dell'invito
    '''
    model = Invito
    form_class = InvitoForm
    login_url = '/utenti/login/'

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
    '''
    View di update dell'invito
    '''
    model = Invito
    form_class = InvitoFormUpdate
    login_url = '/utenti/login/'

    def form_valid(self, form):
        form.instance.utente = self.request.user
        response = super().form_valid(form)
        '''invito = self.get_object()
        for p in invito.partecipanti.all():
            template = render_to_string(
                'inviti/email_update.html',
                {
                    'name': p,
                    'invito': invito,
                }
            )
            email = EmailMessage(
                'Attenzione! Prenotazione modificata',
                template,
                settings.EMAIL_HOST_USER,
                [p.email]
                )
            email.fail_silently = False
            email.send()'''
        return response

    def test_func(self):
        invito = self.get_object()
        if self.request.user == invito.utente:
            return True
        return False


class InvitoPartecipa(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    View di partecipazione: l'utente autenticato può richiedere di partecipare se non autore dell'invito e se
    il numero di posti rimasti è > 0.
    Vengono quindi aggiornati il campo partecipanti dell'invito e l'elenco degli utenti partecipanti alla chat.
    '''
    model = Invito
    template_name = 'inviti/partecipa.html'
    fields = []
    login_url = '/utenti/login/'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=self.request.user.id)
        return context


class InvitoRimuoviPartecipa(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    View di rimozione partecipazione: l'utente autenticato che è già tra i partecipanti può annullare la prenotazione.
    Vengono quindi aggiornati il campo partecipanti dell'invito e l'elenco degli utenti partecipanti alla chat.
    '''
    model = Invito
    template_name = 'inviti/rimuovi_partecipazione.html'
    fields = []
    login_url = '/utenti/login/'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=self.request.user.id)
        return context


# ---------------    DELETE VIEWS    ---------------

class InvitoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    View di cancellazione dell'invito
    '''
    model = Invito
    context_object_name = 'invito'
    success_url = '/inviti/'
    login_url = '/utenti/login/'

    def test_func(self):
        invito = self.get_object()
        if self.request.user == invito.utente:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.get(pk=self.request.user.id)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        '''for p in self.object.partecipanti.all():
            template = render_to_string(
                'inviti/email_delete.html',
                {
                    'name': p,
                    'invito': self.object,
                }
            )
            email = EmailMessage(
                'Attenzione! Prenotazione rimossa',
                template,
                settings.EMAIL_HOST_USER,
                [p.email]
            )
            email.fail_silently = False
            email.send()'''
        self.object.delete()
        return HttpResponseRedirect(success_url)
