import re

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import magic
from static import GeoList, GenreList
from utenti.models import Profile

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
MIME_TYPES = ['image/jpeg', 'image/png']
CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "5242880"

class UserForm(forms.ModelForm):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, label="Nome")
    last_name = forms.CharField(max_length=30, label="Cognome")
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password'}))
    conferma_password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'conferma_password',
                  'first_name',
                  'last_name',
                  'email')



    def clean_username(self):
        if not re.match("^[A-Za-z0-9]+$", self.cleaned_data['username']):
            return 'Errore: lo username può contenere solo lettere e numeri.'
        if not (3 <= len(self.cleaned_data['username']) <= 30):
            return 'Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'
        return self.cleaned_data['username']

    def clean_password(self):
        # controllo password
        if not re.match("^[A-Za-z0-9èòàùì]+$", self.cleaned_data['password']):
            raise ValidationError(_('Errore: la password può contenere solo lettere minuscole, maiuscole e numeri.'))
        if not (3 <= len(self.cleaned_data['password']) <= 20):
            raise ValidationError(_('Errore: la password deve avere lunghezza fra 3 e 20 caratteri.'))
        return self.cleaned_data['password']

    def clean_conferma_password(self):
        if not re.match("^[A-Za-z0-9èòàùì]+$", self.cleaned_data['conferma_password']):
            raise ValidationError(
                _('Errore: la conferma password può contenere solo lettere minuscole, maiuscole e numeri.'))
        if not (3 <= len(self.cleaned_data['conferma_password']) <= 20):
            raise ValidationError(_('Errore: la conferma password deve avere lunghezza fra 3 e 20 caratteri.'))
        return self.cleaned_data['conferma_password']

    def clean_first_name(self):
        if not re.match("^[A-Za-z 'èòàùì]+$", self.cleaned_data['first_name']):
            raise ValidationError(_('Errore: il nome può contenere solo lettere.'))
        if not (1 <= len(self.cleaned_data['first_name']) <= 30):
            raise ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        # controllo cognome
        if not re.match("^[A-Za-z 'èòàùì]+$", self.cleaned_data['last_name']):
            raise ValidationError(_('Errore: il cognome può contenere solo lettere.'))
        if not (1 <= len(self.cleaned_data['last_name']) <= 30):
            raise ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
        return self.cleaned_data['last_name']

    def clean_email(self):
        # controllo email
        if not (5 <= len(self.cleaned_data['email']) <= 50):
            raise ValidationError(_('Errore: la mail deve essere compresa gra 5 e 50 caratteri.'))
        return self.cleaned_data['email']


class UtenteCineDateForm(forms.ModelForm):
    required_css_class = 'required'

    sesso=forms.ChoiceField(choices=[('Uomo','Uomo'),('Donna','Donna')])
    generi_preferiti=forms.MultipleChoiceField(choices=GenreList.GenreList.ListaGeneri,
                                               widget=forms.CheckboxSelectMultiple())
    foto_profilo = forms.ImageField(required=False)
    provincia = forms.ChoiceField(choices=GeoList.Anagrafica.ListaProvince)
    regione = forms.ChoiceField(choices=GeoList.Anagrafica.ListaRegioni)

    class Meta:

        model = Profile
        fields = ['indirizzo',
                  'citta',
                  'provincia',
                  'regione',
                  'telefono',
                  'sesso',
                  'data_nascita',
                  'generi_preferiti',
                  'foto_profilo',
                  'guidatore',
                  'posti_macchina'
                  ]

    #    if oauth_user == 1:
    #        del self.fields['password']
    #        del self.fields['conferma_password']
    def clean_indirizzo(self):
        # controllo indirizzo
        if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", self.cleaned_data['indirizzo']):
            raise ValidationError(_('Errore: l\'indirizzo può contenere solo lettere, numeri e /.'))
        if not (3 <= len(self.cleaned_data['indirizzo']) <= 50):
            raise ValidationError(_('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return self.cleaned_data['indirizzo']

    def clean_citta(self):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", self.cleaned_data['citta']):
            raise ValidationError(_('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(self.cleaned_data['citta']) <= 50):
            raise ValidationError(_('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return self.cleaned_data['citta']

    def clean_telefono(self):
        # controllo telefono
        if not re.match("^[0-9]+$", self.cleaned_data['telefono']):
            raise ValidationError(_('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(self.cleaned_data['telefono']) <= 30):
            raise ValidationError(_('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return self.cleaned_data['telefono']

    def clean_foto_profilo(self):
        files = self.files.get('foto_profilo')

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise forms.ValidationError(_("file non supportato."))
            return files
        return None


    def clean_posti_macchina(self):
        if not re.match("^[0-9]$", str(self.cleaned_data['posti_macchina'])):
            raise ValidationError(_('Errore: il numero posti macchina può contenere solo un numero.'))
        if not (0 <= int(self.cleaned_data['posti_macchina']) <= 8):
            raise ValidationError(_('Errore: il numero posti macchina deve essere compresa fra 1 e 8.'))
        return self.cleaned_data['posti_macchina']



"""
class UserModifyForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email')
    def clean_username(self):
        if not re.match("^[A-Za-z0-9]+$", self.cleaned_data['username']):
            return 'Errore: lo username può contenere solo lettere e numeri.'
        if not (3 <= len(self.cleaned_data['username']) <= 30):
            return 'Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'
        return self.cleaned_data['username']

    def clean_first_name(self):
        if not re.match("^[A-Za-z 'èòàùì]+$", self.cleaned_data['first_name']):
            raise ValidationError(_('Errore: il nome può contenere solo lettere.'))
        if not (1 <= len(self.cleaned_data['first_name']) <= 30):
            raise ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        # controllo cognome
        if not re.match("^[A-Za-z 'èòàùì]+$", self.cleaned_data['last_name']):
            raise ValidationError(_('Errore: il cognome può contenere solo lettere.'))
        if not (1 <= len(self.cleaned_data['last_name']) <= 30):
            raise ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
        return self.cleaned_data['last_name']

    def clean_email(self):
        # controllo email
        if not (5 <= len(self.cleaned_data['email']) <= 50):
            raise ValidationError(_('Errore: la mail deve essere compresa gra 5 e 50 caratteri.'))
        return self.cleaned_data['email']
"""