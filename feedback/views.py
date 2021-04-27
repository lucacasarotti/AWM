from datetime import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from feedback.forms import  FeedbackForm
from feedback.models import Recensione
from feedback.serializer import FeedbackModelSerializer
from inviti.models import Invito
from main.views import nega_accesso_senza_profilo
from utenti.models import Profile



class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = 2





@login_required(login_url='/utenti/login/')
def nuovo_feedback(request, oid):
    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:oauth_utente'))

    form = FeedbackForm(request.POST or None)
    user_profile_corrente = Profile.objects.filter(user=request.user).first()
    user_recensito = User.objects.filter(pk=oid).first()
    if user_recensito is None:
        raise Http404

    context = {
        "form": form,
    }

    if Invito.objects.filter(partecipanti__username=user_recensito,utente=user_profile_corrente.user,\
        data__lt=datetime.now() + timedelta(days=1)) |\
        Invito.objects.filter(utente=user_recensito,partecipanti__username=user_profile_corrente.user,
        data__lt=datetime.now() + timedelta(days=1))| \
        Invito.objects.filter(partecipanti__username=user_recensito).filter(partecipanti__username=user_profile_corrente.user) \
          .filter(data__lt=datetime.now() + timedelta(days=1)):
        is_rece_valida = True
    else:
        is_rece_valida = False
        context.update({'error_message': 'Errore: prima di recensire l\'utente devi accettare un suo invito '
                                         'e deve essere trascorso almeno un giorno dalla visione del film'})
    if Recensione.objects.filter(user_recensore=user_profile_corrente.user).filter(user_recensito=user_recensito):
        is_rece_valida = False
        context.update({'error_message': 'Errore: hai già recensito questo utente'})
    if form.is_valid() and is_rece_valida:
        feedback = Recensione.objects.create(user_recensore=user_profile_corrente.user, user_recensito=user_recensito)

        feedback.titolo = form.cleaned_data['titolo']
        feedback.descrizione = form.cleaned_data['descrizione']
        feedback.voto = form.cleaned_data['voto']
        #feedback.timestamp=datetime.now()

        feedback.save()

        return HttpResponseRedirect(reverse('main:index'))

    context.update({'user_feedback':user_recensito})
    return render(request, 'feedback/nuovo_feedback.html', context)




class FeedbackModelViewSet(ModelViewSet):
    queryset = Recensione.objects.all()
    serializer_class = FeedbackModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        """
        CONTROLLARE
        """
        try:
            User.objects.get(id=request.GET['user_recensito'])
        except:
                return HttpResponseNotFound()

        self.queryset = self.queryset.filter(Q(user_recensito=request.GET['user_recensito']))

        page=self.paginate_queryset(self.queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        feedback = get_object_or_404(
            self.queryset.filter(user_recensito=kwargs['oid']).order_by('-timestamp'))
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)