from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from utenti.models import Profile
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from CineDate import settings
from chatroom.models import Room, MessageModel
from django.core.exceptions import PermissionDenied

from chatroom.serializers import MessageModelSerializer, UserModelSerializer


@login_required(login_url='/utenti/login/')
def chat(request,room_id):
    try:
        room=Room.objects.get(id=room_id)
    except:
        raise Http404
    if request.user not in room.users.all():
        raise PermissionDenied

    users = Profile.objects.filter(id__in=room.users.all())

    context = {
        "room": room,
        "utenti": users,
    }
    return render(request, 'chatroom/chat.html', context=context)


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


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        try:
            room = Room.objects.get(id=request.GET['target'])
        except:
            raise Http404
        if request.user in room.users.all():
            self.queryset = self.queryset.filter(Q(recipient=request.GET['target']))
            page=self.paginate_queryset(self.queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied


class RetrieveMessageViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def retrieve(self, request, *args, **kwargs):
        try:
            room = Room.objects.get(id=kwargs['room_name'])
        except:
            raise Http404
        if request.user in room.users.all():
            msg = get_object_or_404(
                self.queryset.filter(Q(recipient=kwargs['room_name']),
                                     Q(pk=kwargs['id'])))
            serializer = self.get_serializer(msg)
            return Response(serializer.data)
        else:
            raise PermissionDenied


