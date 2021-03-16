from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'chatroom/index.html')

def room(request, room_name):
    return render(request, 'chatroom/room.html', {
        'room_name': room_name
    })