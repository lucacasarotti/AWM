from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from utenti.models import User
from inviti.models import Invito
from inviti.api.serializers import InvitoSerializer, InvitoSimpleSerializer

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


# PATH /api/inviti/list/
class ApiInvitiListView(ListAPIView):
    queryset = Invito.objects.all().order_by('data')
    serializer_class = InvitoSerializer
    pagination_class = PageNumberPagination


class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = Invito.objects.all()
        serializer = InvitoSimpleSerializer(qs, many=True)
        return Response(serializer.data)


'''    def post(self, request, *args, **kwargs):
        serializer = InvitoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)'''



