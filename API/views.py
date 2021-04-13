from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from CineDate import settings
from chatroom.models import MessageModel
from feedback.models import Recensione
from .permissions import *
from API.serializers import DatiUtenteCompleti, RecensioniSerializer, CompletaRegUtenteNormale, MessageModelSerializer
from utenti.models import Profile


class userInfoLogin(generics.RetrieveAPIView):
    """
    Questa view restituisce la lista completa degli utenti registrati
    """
    serializer_class = DatiUtenteCompleti

    def get_object(self):
        """
        Modifico il query set in modo da ottenere l'utente con l'id
        prelevato dall'url
        """
        oid = self.kwargs['pk']
        return Profile.objects.get(user=oid)

class selfUserInfoLogin(generics.RetrieveUpdateDestroyAPIView):
    '''
    restituisco di default il profilo dell'utente loggato
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = DatiUtenteCompleti

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def perform_destroy(self, instance):
        profilo_da_eliminare = User.objects.get(id=instance.user.id)
        profilo_da_eliminare.is_active = False
        profilo_da_eliminare.save()
        logout(self.request)



class completaRegUtentenormale(generics.RetrieveUpdateAPIView):
    '''
    completa l'inserimento dei dati per un utente normale
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegUtenteNormale

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class cercaUtente(generics.ListAPIView):
    serializer_class = DatiUtenteCompleti

    def get_queryset(self):
        name = self.kwargs['name']
        profili = []
        try:
            username_cercato = User.objects.get(username__exact=name)
            profilo = Profile.objects.get(user=username_cercato)
            profilo.user.password = ""
            profili.append(profilo)
            return profili
        except Exception:
            username_trovati = User.objects.filter(username__startswith=name)
            if len(username_trovati) == 0:
                username_trovati = User.objects.filter(username__contains=name)
            for user in username_trovati:
                p = Profile.objects.get(user=user)
                p.user.password = ""
                profili.append(p)
            return profili


class recensisciUtente(generics.CreateAPIView):
    serializer_class = RecensioniSerializer
    permission_classes = [IsUserLogged]

    def perform_create(self, serializer):
        nickname_recensore = self.request.user.username

        nickname_recensito = self.kwargs['utente']
        try:
            recensore = User.objects.get(username=nickname_recensore)
        except Exception:
            raise Exception("Utente recensore non trovato")
        try:
            recensito = User.objects.get(username=nickname_recensito)
        except Exception:
            raise Exception("Utente recensito non trovato")

        rec = Recensione.objects.filter(user_recensore=recensore, user_recensito=recensito)
        if len(rec) != 0:
            raise PermissionDenied("hai già recensito l'utente")

        if recensito != recensore:
            serializer.save(user_recensore=recensore, user_recensito=recensito)
        else:
            raise PermissionDenied("non puoi recensire te stesso")


class recensioniRicevute(generics.ListAPIView):
    serializer_class = RecensioniSerializer

    def get_queryset(self):
        # lista_recensioni = []
        nickname_cercato = self.kwargs['utente']
        try:
            recensito = User.objects.get(username=nickname_cercato)
        except Exception:
            raise Exception("Utente recensito non trovato")
        recensioni = Recensione.objects.filter(user_recensito=recensito)
        return list(recensioni)



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

    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(generics.ListCreateAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def get_queryset(self, request, *args, **kwargs):

        self.queryset = self.queryset.filter(Q(recipient=request.GET['target']))
        page=self.paginate_queryset(self.queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return serializer.data


class RetrieveMessageViewSet(generics.ListAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=kwargs['room_name']),
                                 Q(pk=kwargs['id'])))
        serializer = self.get_serializer(msg)
        return serializer.data

