from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from utenti.models import Profile


def nega_accesso_senza_profilo(request):
    """
    Funzione utilizzata dalle view per negare l'accesso agli utenti oauth loggati e sprovvisti di un profilo
    (perchè non hanno completato la registrazione del proprio profilo).

    :param request: request utente.
    :return: render della pagina scelta_profilo_oauth.
    """

    # if request.user.is_authenticated:
    #     try:
    #         Profile.objects.get(user=request.user.id)
    #     except Exception:
    #         return True

    if request.user.is_authenticated:
        profilo = Profile.objects.get(user=request.user.id)
        if len(profilo.indirizzo) == 0:
            return True
    return False


def index(request):
    """
    Mostra la pagina principale del sito, lista annunci.

    :param request: request utente.
    :return: redirect alla view lista_annunci.
    """
    return render(request,'main/index.html',None)
    #da cambiare
    #return HttpResponseRedirect(reverse('utenti:registrazione'))


