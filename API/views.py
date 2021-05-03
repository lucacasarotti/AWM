from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, Value, IntegerField
from django.http import JsonResponse
from django_filters import rest_framework

from rest_framework import generics, exceptions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from CineDate import settings
from chatroom.models import MessageModel, Room
from feedback.models import Recensione
from inviti.models import Invito
from .permissions import *
from API.serializers import DatiUtenteCompleti, RecensioniSerializer, CompletaRegUtente, MessageModelSerializer, \
    RoomModelSerializer, InvitoSerializer, InvitoCreateSerializer, PartecipantiSerializer
from utenti.models import Profile
from inviti.filters import InvitoFilter


class SmallResultsSetPagination(PageNumberPagination):
    """
    Paginazione customizzata a 20 risultati.
    """
    page_size = 20
    page_size_query_param = 'page_size'


# PATH /api/inviti/list/
class InvitiListView(generics.ListAPIView):
    """
    API per la lista di tutti gli inviti futuri.
    La richiesta segue il filtraggio specificao in InvitoFilter.
    """
    pagination_class = SmallResultsSetPagination
    # queryset = Invito.objects.all().order_by('data')
    queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
    serializer_class = InvitoSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = InvitoFilter


# PATH /api/inviti/create/
class InvitoCreateView(generics.CreateAPIView):
    """
    API per la creazione di un invito e room corrispondente.
    """
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
    La view restituisce l'invito avente ID passato.
    La modifica/delete è permessa solo in caso di utente auth e proprietario.
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

    def perform_update(self, serializer):
        invito = self.get_object()
        # update solo se creatore dell'annuncio
        if invito.utente == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied()


# PATH /api/inviti/cerca/<str:titolo>/
class CercaFilm(generics.ListAPIView):
    """
    La view restituisce la lista di inviti il cui film matcha con la stringa titolo passata come parametro.
    Prima controlla che il match esatto, in caso negativo il vincolo di ricerca viene rilassato.
    """
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


# PATH /api/inviti/partecipa/<int:pk>/
class PartecipaInvito(generics.RetrieveUpdateAPIView):
    """
    Questa view serve per gestire la partecipazione ad un invito.
    L'utente autenticato è aggiunto ai partecipanti se non compare nella lista altrimenti viene disiscritto.
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


# PATH /api/inviti/utente/<str:username>/
class InvitiUtenteListView(generics.ListAPIView):
    """
    API per la lista di tutti gli inviti creati dall'utente corrispondente allo username passato come parametro.
    """
    pagination_class = SmallResultsSetPagination
    # queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
    serializer_class = InvitoSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        i = Q(utente=user, data__gte=datetime.today())
        s = Q(utente=user, data__lt=datetime.today())
        inviti = (Invito.objects.filter(i | s).annotate(
            search_type_ordering=Case(When(i, then=Value(1)), When(s, then=Value(0)), default=Value(-1),
                                      output_field=IntegerField(), )).order_by('-search_type_ordering', 'data'))
        return inviti


# PATH /api/inviti/prenotazioni/<str:username>/
class PrenotazioniListView(generics.ListAPIView):
    """
    API per la lista di tutte le prenotazioni dell'utente corrispondente allo username passato come parametro.
    Server-side la lista è visualizzabile da tutti.
    """
    pagination_class = SmallResultsSetPagination
    queryset = Invito.objects.filter(data__gte=datetime.today()).order_by('data')
    serializer_class = InvitoSerializer

    def get_queryset(self):
        i = Q(partecipanti__username=self.kwargs.get('username'), data__gte=datetime.today())
        s = Q(partecipanti__username=self.kwargs.get('username'), data__lt=datetime.today())
        inviti = (Invito.objects.filter(i | s).annotate(
            search_type_ordering=Case(When(i, then=Value(1)), When(s, then=Value(0)), default=Value(-1),
                                      output_field=IntegerField(), )).order_by('-search_type_ordering', 'data'))
        return inviti


# PATH /api/utenti/profilo/<int:pk>/
class userInfoLogin(generics.RetrieveAPIView):
    """
    La view restituisce il profilo corrispondete alla pk passata come parametro.
    """
    serializer_class = DatiUtenteCompleti

    def get_object(self):

        oid = self.kwargs['pk']
        return Profile.objects.get(user=oid)


# PATH /api/utenti/profilo/
class selfUserInfoLogin(generics.RetrieveUpdateDestroyAPIView):
    """
    La view restituisce di default il profilo dell'utente loggato.
    """
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = DatiUtenteCompleti

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def perform_destroy(self, instance):
        profilo_da_eliminare = User.objects.get(id=instance.user.id)
        profilo_da_eliminare.is_active = False
        profilo_da_eliminare.save()
        logout(self.request)


# PATH /api/utenti/registra/utente/
class completaRegUtente(generics.RetrieveUpdateAPIView):
    """
    La view completa l'inserimento dei dati per un utente.
    """
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegUtente

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


# PATH /api/utenti/cerca/<str:name>/
class cercaUtente(generics.ListAPIView):
    """
    La view restituisce la lista di utenti che matchano con la stringa name passata come parametro.
    Prima controlla che l'utente abbia inserito l'esatto username,
    in caso negativo rilassa il vincolo di ricerca.
    """
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

# PATH /api/recensioni/nuova/<str:utente>/
class recensisciUtente(generics.CreateAPIView):
    """
    View che permette di inserire una nuova recensione.
    Per poter eseguire l'operazione viene controllato che il recensito non abbia già ricevuto una recensione dal
    recensore e che ci sia stato tra i due un invito valido (accettato e che sia passato almeno un giorno dalla data
    invito). Controlla anche che il recensore non stia provando a recensirsi da solo.
    """
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
            raise exceptions.PermissionDenied(detail="Hai già recensito l'utente")

        if not Invito.objects.filter(partecipanti__username=recensito, utente=recensore,
                                     data__lt=datetime.now() + timedelta(days=1)) | \
                Invito.objects.filter(utente=recensito, partecipanti__username=recensore,
                                      data__lt=datetime.now() + timedelta(days=1)) | \
                Invito.objects.filter(partecipanti__username=recensito).filter(
                    partecipanti__username=recensore) \
                        .filter(data__lt=datetime.now() + timedelta(days=1)):
            raise exceptions.PermissionDenied(detail="Prima di recensire l\'utente devi accettare un suo invito e "
                                                     "deve essere trascorso almeno un giorno dalla visione del film")
        if recensito != recensore:
            serializer.save(user_recensore=recensore, user_recensito=recensito)
        else:
            raise exceptions.PermissionDenied(detail="Non puoi recensire te stesso")


class SmallPagination(PageNumberPagination):
    """
    Paginazione customizzata a 5 risultati.
    """
    page_size = 5


# PATH /api/recensioni/ricevute/<str:utente>/
class recensioniRicevute(generics.ListAPIView):
    """
    View che restituisce le recensioni ricevute da un utente, il cui username è passato come parametro.
    """
    serializer_class = RecensioniSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
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
    Paginazione customizzata al default specificato nei settings (100).
    """
    page_size = settings.MESSAGES_TO_LOAD


# PATH /api/chat/
class RoomModelViewSet(generics.ListAPIView):
    """
    View che restituisce le chatroom disponibili per un utente.
    """
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsUserLogged, ]
    pagination_class = SmallPagination

    def get_queryset(self):
        rooms_trovate = self.queryset.filter(users=self.request.user)
        i = Q(id__in=rooms_trovate, invito__data__gte=datetime.today())
        s = Q(id__in=rooms_trovate, invito__data__lt=datetime.today())

        rooms_trovate = (Room.objects.filter(i | s).annotate(
            search_type_ordering=Case(When(i, then=Value(1)), When(s, then=Value(0)), default=Value(-1),
                                      output_field=IntegerField(), )).order_by('-search_type_ordering', 'invito__data'))

        return rooms_trovate


# PATH /api/chat/<int:room_name>/messages/
class MessageModelViewSet(generics.ListCreateAPIView):
    """
    View che permette all'utente di recuperare i messaggi della chatroom e di inviarne di nuovi.
    """
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (TokenAuthentication,CsrfExemptSessionAuthentication)
    pagination_class = MessagePagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(Q(recipient=self.kwargs['room_name']))
        return self.queryset


# PATH /api/chat/<int:room_name>/messages/<int:id>/
class RetrieveMessageViewSet(generics.ListAPIView):
    """
    View che gestisce la ricezione da parte degli utenti connessi alla websocket per un nuovo messaggio.
    """
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    authentication_classes = (TokenAuthentication,CsrfExemptSessionAuthentication)
    pagination_class = MessagePagination

    def get_queryset(self):
        msg = self.queryset.filter(Q(recipient=self.kwargs['room_name']),
                                     Q(pk=self.kwargs['id']))
        return msg


# PATH /api/utento/check_username/
def check_username(request):
    """
    Controlla se uno username, passato come parametro GET, non sia già registrato nel model.

    :param request: request utente.
    :return: falso se username già registrato, vero se username non registrato.
    """
    if request.method == "GET":
        p = request.GET.copy()
        if 'username' in p:
            name = p['username']
            if User.objects.filter(username__iexact=name):
                return JsonResponse({'result':False})
            else:
                return JsonResponse({'result':True})

