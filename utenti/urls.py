from django.conf.urls import url
from django.urls import path

from . import views

app_name='utenti'

urlpatterns = [

    path('login/', views.login_user, name='utenti_login'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('logout/',views.logout_user,name='logout_user'),
    path('profilo/<int:oid>/', views.view_profile, name='view_profile'),
    path('profilo/<int:oid>/modifica/', views.edit_profile, name='edit_profile'),
    #path('profilo/<int:oid>>/elimina/', views.elimina_profilo, name='elimina_profilo'),
    #path('profilo/<int:oid>/elimina/conferma/', views.elimina_profilo_conferma, name='elimina_profilo_conferma'),

]