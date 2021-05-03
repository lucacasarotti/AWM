from django.urls import path
from inviti.views import InvitiHome

app_name = 'main'
urlpatterns = [
    path('', InvitiHome.as_view(), name='index'),
]
