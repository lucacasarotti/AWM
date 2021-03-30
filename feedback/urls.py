from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import FeedbackModelViewSet

app_name = 'feedback'

urlpatterns = [

    path(r'feedback-list/', FeedbackModelViewSet.as_view(({'get': 'list',})),name='get_feedback'),

    path('nuovo/<int:oid>/',views.nuovo_feedback,name='nuovo_feedback')
]


