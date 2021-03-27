from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from feedback.forms import RecensioneForm
from feedback.models import Recensione
from inviti.models import Invito
from main.views import nega_accesso_senza_profilo
from utenti.models import Profile


@login_required(login_url='/utenti/login/')
def nuova_recensione(request, oid):

    """
    Permette a un utente di inserire una recensione nei confronti di un altro utente.
    Per poter eseguire l'operazione viene controllato che il recensito non abbia già ricevuto una recensione dal
    recensore e che ci sia stato tra i due un annuncio valido (accettato e con data di fine conclusa).

    :param request: request utente.
    :param oid: id dell'utente recensito.
    :return: render della pagina nuova_recensione.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    form = RecensioneForm(request.POST or None)
    user_profile_corrente = Profile.objects.filter(user=request.user).first()
    user_recensito = User.objects.filter(pk=oid).first()

    if user_recensito is None:
        raise Http404

    context = {
        "form": form,
    }

    if Invito.objects.filter(user=user_recensito).filter(user_accetta=user_profile_corrente.user).\
            filter(data_fine__lt=datetime.now()):
        is_rece_valida = True
    else:
        is_rece_valida = False
        context.update({'error_message': 'Errore: prima di recensire l\'utente devi accettare un suo annuncio '
                                         'e la data di fine deve essere trascorsa'})
    if Recensione.objects.filter(user_recensore=user_profile_corrente.user).filter(user_recensito=user_recensito):
        is_rece_valida = False
        context.update({'error_message': 'Errore: hai già recensito questo utente'})

    if form.is_valid() and is_rece_valida:

        recensione = Recensione.objects.create(user_recensore=user_profile_corrente.user, user_recensito=user_recensito)

        recensione.titolo = form.cleaned_data['titolo']
        recensione.descrizione = form.cleaned_data['descrizione']
        recensione.voto = form.cleaned_data['voto']

        recensione.save()

        return HttpResponseRedirect(reverse('main:index'))

    context.update({'base_template': 'main/base.html'})
    context.update({'user_profile': Profile.objects.filter(user=request.user).first()})

    return render(request, 'recensioni/nuova_recensione.html', context)

def recensioni_ricevute(request, username):

    """
    Mostra l'elenco delle recensioni ricevute da un determinato utente.

    :param request: request utente.
    :param username: username dell'utente di cui mostrare le recensioni ricevute.
    :return: render della pagina recensioni_ricevute.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    utente_richiesto = User.objects.filter(username=username).first()

    try:
        recensioni = Recensione.objects.filter(user_recensito=utente_richiesto.pk)
    except Exception:
        raise Http404

    context = {
        'recensioni': recensioni,
        'username': username,
    }
    if not request.user.is_authenticated():
        context.update({'base_template': 'main/base_visitor.html'})
        return render(request, 'recensioni/recensioni_ricevute.html', context)
    else:
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})
        context.update({'base_template': 'main/base.html'})
        return render(request, 'recensioni/recensioni_ricevute.html', context)
