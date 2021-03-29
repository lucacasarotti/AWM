from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, CharField

from feedback.models import Recensione


class FeedbackModelSerializer(ModelSerializer):

    class Meta:
        model = Recensione
        fields = '__all__'