import re

import magic
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from chatroom.models import Room, MessageModel
from feedback.models import Recensione
from utenti.models import Profile
from utenti.views import calcola_lat_lon
from django.utils.translation import ugettext_lazy as _


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
MIME_TYPES = ['image/jpeg', 'image/png']
CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "5242880"


def aggiornaLatLng(user, request):
    utente_richiedente = Profile.objects.get(user=user)
    latitudine, longitudine = calcola_lat_lon(request, utente_richiedente)
    utente_richiedente.latitudine = latitudine
    utente_richiedente.longitudine = longitudine
    utente_richiedente.save()


def calcolaMediaVotiUtente(profilo):
    utente = User.objects.get(username = profilo)
    somma = 0
    recensioni = Recensione.objects.filter(user_recensito=utente)
    for obj in recensioni:
        somma += obj.voto
    if len(recensioni)!=0:
        media = somma / len(recensioni)
    else:
        media = 0
    return media


def calcolaNumeroVotiUtente(profilo):
    utente = User.objects.get(username = profilo)
    recensioni = Recensione.objects.filter(user_recensito=utente)
    return len(recensioni)

class UsernameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]

    def validate_username(self, data):
        if not re.match("^[A-Za-z0-9]+$", data):
            return serializers.ValidationError(
                _('Errore: lo username può contenere solo lettere e numeri.'))
        if not (3 <= len(data) <= 30):
            return serializers.ValidationError(
                _('Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'))
        return data['username']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude=[
                "last_login",
                "is_superuser",
                "is_staff",
                "is_active",
                "date_joined",
                "groups",
                "user_permissions",
                ]
        read_only_fields = ["id"]
        extra_kwargs = {
                        'username': {
                            'validators': [UnicodeUsernameValidator()],
                        }
        }

        def validate_username(self,data):
            if not re.match("^[A-Za-z0-9_\-]+$", data):
                return serializers.ValidationError(_('Errore: lo username può contenere solo lettere, numeri, - e _.'))
            if not (3 <= len(data) <= 30):
                return serializers.ValidationError(
                    _('Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'))
            return data['username']

        def validate_password(self,data):
            # controllo password
            if not re.match("^[A-Za-z0-9èòàùì_\-!?&]+$", data):
                raise serializers.ValidationError(
                    _('Errore: la password può contenere solo lettere minuscole, maiuscole e numeri.'))
            if not (3 <= len(data) <= 20):
                raise serializers.ValidationError(
                    _('Errore: la password deve avere lunghezza fra 3 e 20 caratteri.'))
            return data

        def validate_conferma_password(self,data):
            if not re.match("^[A-Za-z0-9èòàùì_\-!?&]+$", data):
                raise serializers.ValidationError(
                    _('Errore: la conferma password può contenere solo lettere minuscole, maiuscole e numeri.'))
            if not (3 <= len(data) <= 20):
                raise serializers.ValidationError(_('Errore: la conferma password deve avere lunghezza fra 3 e 20 caratteri.'))
            return data

        def validate_first_name(self, data):
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il nome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_last_name(self, data):
            # controllo cognome
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il cognome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_email(self, data):
            # controllo email
            if not (5 <= len(data) <= 50):
                raise serializers.ValidationError(_('Errore: la mail deve essere compresa gra 5 e 50 caratteri.'))
            return data



class AnagraficaSerializer(serializers.ModelSerializer):
    '''
    classe per effettuare la serializzazione dei dati.
    I Serializers permettono la conversione di tipi di dato complessi come :
    istanze di modelli o queryset in tipi di dato nativi di Python,
    facilitandone il rendering in formati a noi utili come ad esempio JSON
    '''
    foto_profilo = serializers.FileField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields =["id"]


    def validate_indirizzo(self,data):
        # controllo indirizzo
        if not re.match("^[A-Za-z/, 0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri,/ o ,.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self,data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self,data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self,data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None


    def validate_posti_macchina(self,data):
        if not re.match("^[0-9]$", str(data)):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina può contenere solo un numero.'))
        if not (0 <= int(data) <= 8):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina deve essere compresa fra 1 e 8.'))
        return data



class RecensioniSerializer(serializers.ModelSerializer):
    user_recensore = serializers.CharField(max_length=30, allow_null=True, allow_blank=True, required=False)
    user_recensito = serializers.CharField(max_length=30, allow_null=True, allow_blank=True, required=False)
    class Meta:
        model = Recensione
        fields ='__all__'

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 ,.'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: la descrizione può contenere solo lettere, '
                                               'numeri, punti, virgole e spazi.'))
        return data

    def validate_titolo(self, data):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data


class DatiUtenteCompleti(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    numero_recensioni = serializers.SerializerMethodField("get_numero_recensioni_utente")
    media_voti = serializers.SerializerMethodField("get_media_voti_utente")
    foto_profilo = serializers.FileField(read_only=True)
    foto_pet = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        fields =["user",
                 "indirizzo",
                 "citta",
                 "provincia",
                 "regione",
                 "telefono",
                 "foto_profilo",
                 "guidatore",
                 "data_nascita",
                 "posti_macchina",
                 "numero_recensioni",
                 "media_voti",
                 ]

    def validate_indirizzo(self, data):
        # controllo indirizzo
        if not re.match("^[A-Za-z/, 0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri,/ o ,.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self, data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_posti_macchina(self, data):
        if not re.match("^[0-9]$", str(data)):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina può contenere solo un numero.'))
        if not (0 <= int(data) <= 8):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina deve essere compresa fra 1 e 8.'))
        return data

    def get_media_voti_utente(self,profilo):
        # user = Profile.__class__.objects.get(user=self.instance)
        return calcolaMediaVotiUtente(profilo)

    def get_numero_recensioni_utente(self,profilo):
        # user = Profile.__class__.objects.get(user=self.instance)
        return calcolaNumeroVotiUtente(profilo)

    def update(self, instance, validated_data):
        v = instance.user.username
        dati_utente= validated_data.pop('user')
        utente_richiedente = Profile.objects.get(user=instance.user)
        # username, first_name, last_name, email
        instance.user.username = dati_utente['username']
        instance.user.set_password(dati_utente['password'])
        instance.user.first_name = dati_utente['first_name']
        instance.user.last_name = dati_utente['last_name']
        instance.user.email = dati_utente['email']


        instance.indirizzo = validated_data['indirizzo']
        instance.citta =  validated_data['citta']
        instance.regione =  validated_data['regione']
        instance.provincia =  validated_data['provincia']

        instance.telefono =validated_data['telefono']
        instance.data_nascita=validated_data['data_nascita']
        instance.guidatore = validated_data['guidatore']
        instance.posti_macchina = validated_data['posti_macchina']

        instance.user.save()
        instance.save()
        aggiornaLatLng(instance.user, self.context['request'])
        return instance


class CompletaDatiDjangoUser(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude=[
                "last_login",
                "is_superuser",
                "is_staff",
                "is_active",
                "date_joined",
                "groups",
                "user_permissions",
                ]
        read_only_fields = ["id", "email", "username", "password"]


        def validate_first_name(self,data):
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il nome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_last_name(self,data):
            # controllo cognome
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il cognome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data


class CompletaRegUtenteNormale(serializers.ModelSerializer):
    user = CompletaDatiDjangoUser(many=False)
    foto_profilo = serializers.FileField(read_only=True)
    foto_pet = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        exclude = ("latitudine",
                   "longitudine",
                   "id",
                   )

    def validate_indirizzo(self, data):
        # controllo indirizzo
        if not re.match("^[A-Za-z/, 0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri,/ o ,.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self, data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_posti_macchina(self, data):
        if not re.match("^[0-9]$", str(data)):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina può contenere solo un numero.'))
        if not (0 <= int(data) <= 8):
            raise serializers.ValidationError(
                _('Errore: il numero posti macchina deve essere compresa fra 1 e 8.'))
        return data

    def update(self, instance, validated_data):
        v = instance.user.username
        dati_utente = validated_data.pop('user')
        utente_richiedente = Profile.objects.get(user=instance.user)
        # username, first_name, last_name, email
        instance.user.username = dati_utente['username']
        instance.user.set_password(dati_utente['password'])
        instance.user.first_name = dati_utente['first_name']
        instance.user.last_name = dati_utente['last_name']
        instance.user.email = dati_utente['email']

        instance.indirizzo = validated_data['indirizzo']
        instance.citta = validated_data['citta']
        instance.regione = validated_data['regione']
        instance.provincia = validated_data['provincia']

        instance.telefono = validated_data['telefono']
        instance.data_nascita = validated_data['data_nascita']
        instance.guidatore = validated_data['guidatore']
        instance.posti_macchina = validated_data['posti_macchina']

        instance.user.save()
        instance.save()
        aggiornaLatLng(instance.user, self.context['request'])
        return instance

class MessageModelSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', read_only=True)
    recipient = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            Room, id=validated_data['recipient'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')