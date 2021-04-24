from rest_framework import serializers
from inviti.models import Invito
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]


class StringListField(serializers.ListField):
    genere = serializers.CharField()


class InvitoSerializer(serializers.ModelSerializer):
    utente = UserSerializer()
    data = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    orario = serializers.TimeField(format="%H:%M", input_formats=['%H:%M', 'iso-8601'])
    posti_rimasti = serializers.ReadOnlyField()
    genere = StringListField()
    scaduto = serializers.ReadOnlyField()
    partecipanti = UserSerializer(many=True)

    class Meta:
        model = Invito
        fields = '__all__'


class InvitoSimpleSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    orario = serializers.TimeField(format="%H:%M", input_formats=['%H:%M', 'iso-8601'])
    genere = StringListField()

    class Meta:
        model = Invito
        fields = '__all__'


class InvitoCreateSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    orario = serializers.TimeField(format="%H:%M", input_formats=['%H:%M', 'iso-8601'])
    genere = StringListField()

    class Meta:
        model = Invito
        fields = ['data', 'orario', 'genere', 'tipologia', 'cinema', 'film', 'limite_persone', 'commento']


class PartecipantiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invito
        fields = ['partecipanti']

