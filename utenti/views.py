import json
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from CineDate import settings
from main.views import nega_accesso_senza_profilo
from static import GenreList
from utenti.forms import UserForm
from utenti.forms import UtenteCineDateForm
from utenti.models import Profile
import requests

def calcola_lat_lon(request, profile):


    response = requests.get('https://open.mapquestapi.com/geocoding/v1/address?'
                            'key=pnGtLbDVt29CZbfiqMMyjUmZHACj4gNX&location=' + profile.indirizzo.replace("/", "")
                            + ',' + profile.citta.replace("/", "") + ',' + profile.provincia.replace("/", "") +
                            ',' + profile.regione.replace("/", ""))
    latlong = response.json()
    return latlong['results'][0]['locations'][0]['latLng']["lat"], \
        latlong['results'][0]['locations'][0]['latLng']["lng"]


def login_user(request):

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

    if nega_accesso_senza_profilo(request):
       return HttpResponseRedirect(reverse('utenti:oauth_utente'))
    form = UserForm(request.POST or None,oauth_user=0)
    cineform = UtenteCineDateForm(request.POST or None, request.FILES or None)

    if form.is_valid() and cineform.is_valid() and \
            not User.objects.filter(username=form.cleaned_data['username']).exists():

        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        email=form.cleaned_data['email']
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        user = User.objects.create_user(username, email, password, first_name=first_name,last_name=last_name)
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
        profile.data_nascita=cineform.cleaned_data['data_nascita']
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

    return  render(request, 'utenti/registrazione.html', context)
    #if not request.user.is_authenticated:
    #    base_template = 'main/base_site.html'
    #    return render(request, 'utenti/registrazione.html', {'base_template': base_template})
    #else:
    #    return HttpResponseRedirect(reverse('main:index'))
@login_required(login_url='/utenti/login')
def logout_user(request):

    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def view_profile(request,oid):
    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:oauth_utente'))
    user = User.objects.filter(id=oid).first()

    if user is None:
        raise Http404

    user_profile = Profile.objects.filter(user=user.pk).first()
    if user_profile is None:
        raise Http404
    user_profile.generi_preferiti=user_profile.generi_preferiti.replace('[','').replace(']','').replace("\'",'')
    context = {
        'view_user': user,
        'user_profile': user_profile,
        'base_template': 'main/base_site.html'
    }
    return render(request, 'utenti/profilo.html', context)


@login_required(login_url='/utenti/login/')
def edit_profile(request, oid):

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:oauth_utente'))

    context = {'base_template': 'main/base_site.html'}
    oauth_user=False
    if int(oid) == int(request.user.pk):
        user_profile = User.objects.filter(id=oid).first()
        if user_profile.has_usable_password():
            form = UserForm(data=request.POST or None, instance=request.user, oauth_user=0)
        else:
            form = UserForm(data=request.POST or None, instance=request.user, oauth_user=1)
            oauth_user = True

        profile = Profile.objects.filter(user=user_profile.pk).first()
        profile_form=UtenteCineDateForm(data=request.POST or None, instance=profile,files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            if not oauth_user:
                if form.cleaned_data['password'] != form.cleaned_data['conferma_password']:

                    context.update({'form': form})
                    context.update({'profileForm': profile_form})
                    context.update({'error_message': 'Errore: le due password inserite non corrispondono'})

                    return render(request, 'utenti/modifica_profilo.html', context)

            profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)

            if "foto_profilo-clear" in request.POST:
                profile.foto_profilo=None
            user = form.save(commit=False)
            if not oauth_user:
                password = form.cleaned_data['password']
                user.set_password(password)
            form.save()
            profile_form.save()
            if not oauth_user:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                if user.is_active:
                    if not oauth_user:
                        login(request, user)
                    return HttpResponseRedirect(reverse('utenti:view_profile',args=(user.pk,)))
        else:
            try:
                if User.objects.exclude(pk=request.user.id).get(username=form['username'].value()):
                    context.update({'form': form})
                    context.update({'profileForm': profile_form})
                    context['user_profile'] = profile

                    return render(request, 'utenti/modifica_profilo.html', context)
            except User.DoesNotExist:
                # Nessun utente trovato con questo username --> username valido
                pass

            if oauth_user:
                form = UserForm(instance=request.user, oauth_user=1)
            else:
                form = UserForm(instance=request.user, oauth_user=0)
            profile_form = UtenteCineDateForm(instance=profile)

        context.update({'form': form})
        context.update({'profileForm': profile_form})
        context['user_profile'] = profile

        return render(request, 'utenti/modifica_profilo.html', context)

    else:
        raise Http404


@login_required(login_url='/utenti/login/')
def elimina_profilo(request, oid):
    """
    Permette agli utenti di eliminare il proprio profilo, mostrando prima una pagina di conferma.

    :param request: request utente.
    :param oid: id dell'utente da eliminare (con controllo che sia == all'id dell'utente loggato).
    :return: render della pagina elimina_profilo.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:oauth_utente'))

    user = User.objects.filter(id=oid).first()
    if user == User.objects.get(username=request.user):
        context = {'user': user, 'base_template': 'main/base_site.html'}

        return render(request, 'utenti/elimina_profilo.html', context)
    else:
        raise Http404


@login_required(login_url='/utenti/login/')
def elimina_profilo_conferma(request, oid):
    """
    Dopo aver confermato, elimina effettivamente il profilo utente.

    :param request: request utente.
    :param oid: id dell'utente da eliminare.
    :return: render della pagina principale.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:oauth_utente'))

    user = User.objects.filter(id=oid).first()

    if user == User.objects.get(username=request.user):
        User.objects.filter(id=oid).delete()
    else:
        raise Http404

    return HttpResponseRedirect(reverse('main:index'))

@login_required(login_url='/utenti/login/')
def oauth_utente(request):


    if nega_accesso_senza_profilo(request) == False:
        Profile.objects.get(user=request.user.id)
        return HttpResponseRedirect(reverse('main:index'))

    # Se la richiesta è di tipo POST, allora possiamo processare i dati
    if request.method == "POST":
        # Creiamo l'istanza del form e la popoliamo con i dati della POST request (processo di "binding")
        cineform = UtenteCineDateForm(request.POST, request.FILES)

        if cineform.is_valid():
            # a questo punto possiamo usare i dati validi
            utente_loggato = User.objects.get(id=request.user.id)
            profile = Profile.objects.get_or_create(user=utente_loggato)
            profile = profile[0]
            try:
                profile.foto_profilo = request.FILES['foto_profilo']
            except Exception:
                profile.foto_profilo = None

            profile.indirizzo = cineform.cleaned_data['indirizzo']
            profile.citta = cineform.cleaned_data['citta']
            profile.provincia = cineform.cleaned_data['provincia']
            profile.regione = cineform.cleaned_data['regione']
            profile.telefono = cineform.cleaned_data['telefono']
            profile.generi_preferiti = cineform.cleaned_data['generi_preferiti']
            profile.guidatore = cineform.cleaned_data['guidatore']
            profile.posti_macchina = cineform.cleaned_data['posti_macchina']
            profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)
            profile.data_nascita = cineform.cleaned_data['data_nascita']
            profile.sesso = cineform.cleaned_data['sesso']

            profile.save()
            if utente_loggato is not None:
                if utente_loggato.is_active:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        cineform = UtenteCineDateForm()

    # arriviamo a questo punto se si tratta della prima volta che la pagina viene richiesta(con metodo GET),
    # o se il form non è valido e ha errori
    context = {
        "profileForm": cineform,
        "base_template": "main/base_site.html"
    }
    return render(request, 'utenti/oauth_profilo.html', context)
