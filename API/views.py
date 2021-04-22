from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from CineDate import settings
from chatroom.models import MessageModel,Room
from feedback.models import Recensione
from .permissions import *
from API.serializers import DatiUtenteCompleti, RecensioniSerializer, CompletaRegUtenteNormale, MessageModelSerializer, \
    RoomModelSerializer
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


class RoomModelViewSet(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsUserLogged,]
    def get_queryset(self):
        rooms_trovate = self.queryset.filter(users=self.request.user)
        return rooms_trovate


class MessageModelViewSet(generics.ListCreateAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (TokenAuthentication,CsrfExemptSessionAuthentication)
    pagination_class = MessagePagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(Q(recipient=self.kwargs['room_name']))
        return self.queryset



class RetrieveMessageViewSet(generics.ListAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (TokenAuthentication,CsrfExemptSessionAuthentication)
    pagination_class = MessagePagination

    def get_queryset(self):


        msg=self.queryset.filter(Q(recipient=self.kwargs['room_name']),
                                     Q(pk=self.kwargs['id']))
        return msg




def check_username(request):
    """
    Controlla se uno username passato come parametro GET non sia già registrato nel model.

    :param request: request utente.
    :return: False (username già registrato), True (username non registrato).
    """

    if request.method == "GET":
        p = request.GET.copy()
        if 'username' in p:
            name = p['username']
            if name == request.user.username:
                return JsonResponse({'result':True})
            if User.objects.filter(username__iexact=name):
                return JsonResponse({'result':False})
            else:
                return JsonResponse({'result':True})

