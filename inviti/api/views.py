from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import ListAPIView

from utenti.models import User
from inviti.models import Invito
from inviti.api.serializers import InvitoSerializer

@api_view(['GET', ])
def api_detail_invito_view(request, pk):

    try:
        invito = Invito.objects.get(pk=pk)
    except Invito.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvitoSerializer(invito)
        return Response(serializer.data)


'''class ApiInvitiListView(ListAPIView):
    queryset = Invito.objects.all().order_by('data')
    serializer_class = InvitoSerializer
    pagination_class = PageNumberPagination'''


class ApiInvitiListView(ListAPIView):
    queryset = Invito.objects.all().order_by('data')
    serializer_class = InvitoSerializer
    pagination_class = PageNumberPagination


