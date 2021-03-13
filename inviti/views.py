from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Invito
from django import forms


def about(request):
    return render(request, 'inviti/about.html', {'title': 'About'})

# ---------------    LIST VIEWS    ---------------
# add list by genre


def home(request):
    context = {
        'inviti': Invito.objects.all()
    }
    return render(request, 'inviti/home.html', context)


class InvitoListView(ListView):
    model = Invito
    template_name = 'inviti/home.html'
    context_object_name = 'inviti'
    ordering = ['-data_invito']
    paginate_by = 5     # paginate by 5 inviti
    # <name>ListView.as_view() looks for <app>/<model>_<viewtype>.html
    # we need to specify it's home.html
    # we also need to specify that the list is named 'inviti', otherwile to it it has to be called objectslist
    # we use a 'ordering' attribute


class UtenteInvitoListView(ListView):
    '''
    Questa classe serve a visualizzare tutti i post di un utente
    '''
    model = Invito
    template_name = 'inviti/inviti_utente.html'
    context_object_name = 'inviti'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Invito.objects.filter(utente=user).order_by('-data_invito')


# ---------------    DETAIL VIEWS    ---------------

class InvitoDetailView(DetailView):
    model = Invito
    context_object_name = 'invito'

    # template --> looks for <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invito = self.get_object()
        if invito.posti_rimasti != invito.limite_persone:
            context['partecipanti_attuali'] = invito.partecipanti.all()
        return context


# ---------------    CREATE VIEWS    ---------------
'''
class InvitoForm(forms.ModelForm):
    class Meta:
        model = Invito
        fields = ['data', 'orario', 'limite_persone', 'genere', 'commento']
        widgets = {

        }
'''


class InvitoCreateView(LoginRequiredMixin, CreateView):
    # form_class = InvitoForm
    model = Invito
    fields = ['cinema', 'film', 'data', 'orario', 'limite_persone', 'genere', 'commento']

    # template --> looks for <app>/<model>_<viewtype>.html

    def form_valid(self, form):
        form.instance.utente = self.request.user
        return super().form_valid(form)


# ---------------    UPDATE VIEWS    ---------------

class InvitoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invito
    fields = ['cinema', 'film', 'data', 'orario', 'limite_persone', 'genere', 'commento']
    # template --> looks for <app>/<model>_<viewtype>.html

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
    fields = ['partecipanti']

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        utente = self.request.user
        invito = self.get_object()
        invito.partecipanti.add(utente.id)
        invito.save()
        return redirect_url

    def test_func(self):
        invito = self.get_object()
        if self.request.user != invito.utente and invito.posti_rimasti > 0 and self.request.user not in invito.partecipanti.all():
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
