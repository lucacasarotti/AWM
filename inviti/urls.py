from django.urls import path
from . import views

#app_name = 'inviti'
urlpatterns = [
    path('', views.home, name='inviti-home'),
    path('about/', views.about, name='inviti-about'),
]
