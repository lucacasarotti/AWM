from django.contrib import admin
from chatroom.models import MessageModel, Room

"""
class MessageModelAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'body')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'
"""
admin.site.register(MessageModel)

"""
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','title','staff_only']
    search_fields = ['id', 'title']
"""
admin.site.register(Room)