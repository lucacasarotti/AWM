from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from datetime import datetime
from inviti.models import Invito
from utenti.models import Profile, User
from chatroom.models import Room
from inviti.api.serializers import InvitoSerializer, InvitoSimpleSerializer, PartecipantiSerializer, InvitoCreateSerializer
from django.core.exceptions import PermissionDenied
from .permissions import IsCreatorOrReadOnly, IsUserLogged, IsCompatibleUser


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


# PATH /api/inviti/list/
class InvitiListView(generics.ListAPIView):
    '''
    API per la lista di tutti gli inviti futuri
    '''
    pagination_class = SmallResultsSetPagination
    # queryset = Invito.objects.all().order_by('data')
    queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
    serializer_class = InvitoSerializer


# PATH /api/inviti/create/
class InvitoCreateView(generics.CreateAPIView):
    '''
    API per la creazione di un invito
    '''
    permission_classes = [IsUserLogged]
    serializer_class = InvitoCreateSerializer
    queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')

    def perform_create(self, serializer):
        invito = serializer.save(utente=self.request.user)
        room = Room(title=invito.film, invito=invito)
        room.save()
        room.users.add(self.request.user)
        room.save()


# PATH /api/inviti/detail/<pk>/
class InvitoDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Questa view restituisce l'invito avente ID passato
    La modifica/delete è permessa solo in caso di utente auth e proprietario
    """
    serializer_class = InvitoSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_object(self):
        oid = self.kwargs['pk']
        return Invito.objects.get(pk=oid)

    def perform_destroy(self, instance):
        invito = Invito.objects.get(pk=instance.pk)
        # elimina solo se creatore dell'annuncio
        if invito.utente == self.request.user:
            invito.delete()
        else:
            raise PermissionDenied()


# PATH /api/inviti/cerca/<str:titolo>/
class CercaFilm(generics.ListAPIView):
    serializer_class = InvitoSerializer

    def get_queryset(self):
        film = self.kwargs['titolo']
        inviti_validi = Invito.objects.filter(data__gte=datetime.today())
        titoli = []
        try:
            titolo_cercato = inviti_validi.get(film__exact=film)
            titoli.append(titolo_cercato)
            return titoli
        except Exception:
            titoli_trovati = inviti_validi.filter(film__startswith=film)
            if len(titoli_trovati) == 0:
                titoli_trovati = inviti_validi.filter(film__contains=film)
            for i in titoli_trovati:
                titoli.append(i)
            return titoli


# PATH /api/inviti/partecipa/<pk>/
class PartecipaInvito(generics.RetrieveUpdateAPIView):
    """
    Questa view serve per partecipare all'invito se non si è già tra i partecipanti oppure per disiscriversi se lo si è già
    """
    serializer_class = PartecipantiSerializer
    permission_classes = [IsCompatibleUser, IsUserLogged]

    def get_object(self):
        oid = self.kwargs['pk']
        return Invito.objects.get(pk=oid)

    def perform_update(self, serializer):
        oid = self.kwargs['pk']
        invito = Invito.objects.get(id=oid)

        if self.request.user != invito.utente:
            if invito.posti_rimasti > 0 and self.request.user not in invito.partecipanti.all():
                invito.partecipanti.add(self.request.user.id)
                invito.save()
                room = Room.objects.filter(invito=invito)
                if room:
                    room = room[0]
                    room.users.add(self.request.user)
                    room.save()
            elif self.request.user in invito.partecipanti.all():
                invito.partecipanti.remove(self.request.user.id)
                invito.save()
                room = Room.objects.filter(invito=invito)
                if room:
                    room = room[0]
                    room.users.remove(self.request.user)
                    room.save()
        else:
            raise PermissionDenied()


'''
We inherit from
- CreateModelMixin: uses method create which checks validity 
- ListModelMixin: uses method list which gets qs, serializer and paginates
'''
class TestView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView):
    # there is also the get_serializer_class -> if it depends on the request method ecc
    serializer_class = InvitoSimpleSerializer
    # either you specify it ore use get queryset if it depends on the request
    queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')

    # need to specify GET and POST, otherwise no method allowed

    # adding ListModelMixin --> analog to get previously done with list method
    def get(self, request, *args, **kwargs):
        # get request --> returns response to method list
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

