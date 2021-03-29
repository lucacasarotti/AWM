from inviti.api.views import api_detail_invito_view, ApiInvitiListView
from django.urls import path


app_name = 'inviti'

urlpatterns = [
    path('list/', ApiInvitiListView.as_view(), name="list-view"),
    path('<pk>/', api_detail_invito_view, name="detail-view"),
]