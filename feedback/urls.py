from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import FeedbackModelViewSet

app_name = 'feedback'
router = DefaultRouter()
router.register(r'feedback',FeedbackModelViewSet , basename='feedback-api')
urlpatterns = [

    path(r'api/v1/', include(router.urls)),

    path('nuovo/<int:oid>/',views.nuovo_feedback,name='nuovo_feedback')
]


