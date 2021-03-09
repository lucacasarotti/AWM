from django.urls import path
from . import views
from .views import (
    InvitoListView,
    InvitoDetailView,
    InvitoCreateView,
    InvitoUpdateView,
    InvitoDeleteView,
    UtenteInvitoListView,
    InvitoJoinView
)

#app_name = 'inviti'
urlpatterns = [
    #path('', views.home, name='inviti-home'),
    # /inviti/
    path('', InvitoListView.as_view(), name='inviti-home'),
    # /inviti/utente/<username>
    path('utente/<str:username>', UtenteInvitoListView.as_view(), name='inviti-utente'),
    # /inviti/invito/<id_invito>
    path('invito/<int:pk>/', InvitoDetailView.as_view(), name='invito-detail'),
    # /inviti/invito/<id_invito>/partecipa
    path('invito/<int:pk>/partecipa/', InvitoJoinView.as_view(), name='invito-partecipa'),
    # /inviti/nuovo
    path('nuovo/', InvitoCreateView.as_view(), name='invito-create'),
    # /inviti/invito/<id_invito>/update
    path('invito/<int:pk>/update/', InvitoUpdateView.as_view(), name='invito-update'),
    # /inviti/invito/<id_invito>/delete
    path('invito/<int:pk>/delete/', InvitoDeleteView.as_view(), name='invito-delete'),
    # /inviti/about/
    path('about/', views.about, name='inviti-about'),
]
