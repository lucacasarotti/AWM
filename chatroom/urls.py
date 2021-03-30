from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views
from .views import MessageModelViewSet, RetrieveMessageViewSet

app_name = 'chatroom'

urlpatterns = [
    path('<int:room_name>/messages/', MessageModelViewSet.as_view(({'get': 'list','post':'create'})),name='get-messages'),
    path('<int:room_name>/messages/<int:id>/', RetrieveMessageViewSet.as_view(({'get': 'retrieve',})),
         name='get-new_message'),

    #path('<str:room_name>/', login_required(
    #    TemplateView.as_view(template_name='chatroom/chat.html')), name='home'),
    path('<int:room_id>/',views.chat, name='chat')
]