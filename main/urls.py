from django.urls import path
from . import views
app_name='main'
urlpatterns = [
    # /main/
    path('', views.index, name='index'),

]