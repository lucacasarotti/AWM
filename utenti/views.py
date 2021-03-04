from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from main.views import nega_accesso_senza_profilo
from utenti.forms import UserForm
from utenti.forms import UtenteCineDateForm
from utenti.models import Profile


def calcola_lat_lon(request, profile):
    """
    Dato il profilo di un utente con i dati relativi alla sua residenza, viene fatta una query a un API esterna che
    recupera latitudine e longitudine relative alla posizione dell'utente.

    :param request: request utente.
    :param profile: profilo utente.
    :return: latitudine, longitudine restituite dall'API.
    """

    response = requests.get('https://open.mapquestapi.com/geocoding/v1/address?'
                            'key=pnGtLbDVt29CZbfiqMMyjUmZHACj4gNX&location=' + profile.indirizzo.replace("/", "")
                            + ',' + profile.citta.replace("/", "") + ',' + profile.provincia.replace("/", "") +
                            ',' + profile.regione.replace("/", ""))
    latlong = response.json()
    return latlong['results'][0]['locations'][0]['latLng']["lat"], \
        latlong['results'][0]['locations'][0]['latLng']["lng"]


def login_user(request):
    """
    Permette agli utenti di effettuare il login.

    :param request: request utente.
    :return: render della pagina login.
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:index'))
                else:
                    return render(request, 'utenti/login.html', {'error_message': 'Il tuo account è stato disattivato'})
            else:

                return render(request, 'utenti/login.html', {'error_message': 'Login invalido'})
        else:
            return render(request, 'utenti/login.html')


def registrazione(request):
    """
    Permette agli utenti di registrarsi al sito.

    :param request: request utente.
    :return: render della pagina di registrazione o redirect a pagina principale.
    """

    #if nega_accesso_senza_profilo(request):
    #    return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))
    form = UserForm(request.POST or None)
    cineform = UtenteCineDateForm(request.POST or None, request.FILES or None)
    if form.is_valid() and cineform.is_valid() and \
            not User.objects.filter(username=form.cleaned_data['username']).exists():
        user=form.save(commit=False)
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user.save()
        profile=Profile.objects.get(user=user)
        try:
            profile.foto_profilo=request.FILES['foto_profilo']
        except Exception:
            profile.foto_profilo=None
        profile.indirizzo=cineform.cleaned_data['indirizzo']
        profile.citta = cineform.cleaned_data['citta']
        profile.provincia = cineform.cleaned_data['provincia']
        profile.regione = cineform.cleaned_data['regione']
        profile.telefono = cineform.cleaned_data['telefono']
        profile.generi_preferiti=cineform.cleaned_data['generi_preferiti']
        profile.guidatore=cineform.cleaned_data['guidatore']
        profile.posti_macchina=cineform.cleaned_data['posti_macchina']
        profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)
        profile.eta=cineform.cleaned_data['eta']
        profile.sesso=cineform.cleaned_data['sesso']
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))

    context={
        "form":form,
        "profileForm":cineform,
    }
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))

    return  render(request,'utenti/prova.html',{'form_user':form,
                                                'form_cine':cineform})
    #if not request.user.is_authenticated:
    #    base_template = 'main/base_visitor.html'
    #    return render(request, 'utenti/registrazione.html', {'base_template': base_template})
    #else:
    #    return HttpResponseRedirect(reverse('main:index'))
@login_required(login_url='/utenti/login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def view_profile(request,oid):
    pass
