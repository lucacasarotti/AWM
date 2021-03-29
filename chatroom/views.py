from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from CineDate import settings
from chatroom.models import Room
from django.core.exceptions import PermissionDenied

@login_required()
def chat(request,room_id):
    room=Room.objects.get(id=room_id)
    if request.user not in room.users.all():
        raise PermissionDenied

    context = {
        "room": room,
    }
    return render(request, 'chatroom/chat.html',context=context)