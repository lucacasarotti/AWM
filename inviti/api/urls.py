from inviti.api.views import InvitiListView, TestView, InvitoCreateView, InvitoDetailUpdateDelete, PartecipaInvito
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'inviti'

urlpatterns = [
    path('list/', InvitiListView.as_view(), name="api-list-view"),
    path('create/', InvitoCreateView.as_view(), name="api-create-view"),
    path('detail/<pk>/', InvitoDetailUpdateDelete.as_view(), name="api-detail-view"),
    path('partecipa/<pk>/', PartecipaInvito.as_view(), name="api-partecipa-view"),

    path('test/', TestView.as_view(), name="api-test"),

    path('test/token/', obtain_auth_token, name='obtain-token'),
    path('test/api-auth/', include('rest_framework.urls')),
    path('test/rest-auth/', include('rest_auth.urls')),
]