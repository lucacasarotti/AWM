from django.urls import path


from . import views
from .views import MessageModelViewSet, RetrieveMessageViewSet

app_name = 'chatroom'

urlpatterns = [
    path('<int:room_name>/messages/', MessageModelViewSet.as_view(({'get': 'list','post':'create'})),name='get-messages'),
    path('<int:room_name>/messages/<int:id>/', RetrieveMessageViewSet.as_view(({'get': 'retrieve'})),
         name='get-new_message'),

    path('<int:room_id>/',views.chat, name='chat')
]