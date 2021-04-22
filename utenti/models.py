

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.templatetags.static import static
from multiselectfield import MultiSelectField

from static import GenreList


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.CharField(max_length=100)
    citta = models.CharField(max_length=50)

    sesso=models.CharField(max_length=10,default="")
    data_nascita=models.DateField(null=True)
    provincia = models.CharField(max_length=2)
    regione = models.CharField(max_length=50)
    latitudine = models.FloatField(null=True, default=0, blank=True)
    longitudine = models.FloatField(null=True, default=0, blank=True)
    telefono = models.CharField(blank=True,max_length=20)
    foto_profilo = models.FileField(null=True, default='', blank=True)

    guidatore = models.BooleanField(default=False)
    posti_macchina=models.PositiveSmallIntegerField(default=0)

    generi_preferiti =MultiSelectField(null=True,max_length=300, choices=GenreList.GenreList.ListaGeneri)

    feedback_user=models.FloatField(default=0)
    feedback_guidatore=models.FloatField(default=0)

    def __str__(self):
        return self.user.username



    def foto_profilo_or_default(self, default_path=static("/images/user_default.jpg")):
        if self.foto_profilo:

            return settings.MEDIA_URL + str(self.foto_profilo)
        return default_path
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'