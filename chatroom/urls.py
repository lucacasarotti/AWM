from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views
from .api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')


urlpatterns = [
    path(r'<str:room_name>/api/v1/', include(router.urls)),
    #path('<str:room_name>/', login_required(
    #    TemplateView.as_view(template_name='chatroom/chat.html')), name='home'),
    path('<int:room_id>/',views.chat, name='chat')
]