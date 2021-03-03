from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from main.views import nega_accesso_senza_profilo
from utenti.forms import UserForm
from utenti.forms import UtenteCineDateForm




def registrazione(request):
    """
    Permette agli utenti di registrarsi al sito.

    :param request: request utente.
    :return: render della pagina di registrazione o redirect a pagina principale.
    """

    #if nega_accesso_senza_profilo(request):
    #    return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))
    form_user=UserForm()
    form_cine=UtenteCineDateForm()

    return  render(request,'utenti/prova.html',{'form_user':form_user,
                                                'form_cine':form_cine})
    #if not request.user.is_authenticated:
    #    base_template = 'main/base_visitor.html'
    #    return render(request, 'utenti/registrazione.html', {'base_template': base_template})
    #else:
    #    return HttpResponseRedirect(reverse('main:index'))
