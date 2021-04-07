from inviti.api.views import api_detail_invito_view, ApiInvitiListView, TestView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'inviti'

urlpatterns = [
    path('list/', ApiInvitiListView.as_view(), name="api-list-view"),
    path('test/', TestView.as_view(), name="api-test"),
    path('detail/<pk>/', api_detail_invito_view, name="api-detail-view"),
    path('test/token/', obtain_auth_token, name='obtain-token')

]