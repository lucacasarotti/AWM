from django.conf.urls import url
from django.urls import path

from . import views

app_name='utenti'

urlpatterns = [

    path('login/', views.login_user, name='utenti_login'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('logout/',views.logout_user,name='logout_user'),
    path('profilo/<int:oid>/', views.view_profile, name='view_profile')
]