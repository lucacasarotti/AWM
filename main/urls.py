from django.urls import path
from . import views
from inviti.views import InvitoListView

app_name='main'
urlpatterns = [
    # /
    path('', InvitoListView.as_view(), name='index'),
    # path('', views.index, name='index'),

]