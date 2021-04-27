from django.contrib import admin
from chatroom.models import MessageModel, Room


admin.site.register(MessageModel)

admin.site.register(Room)