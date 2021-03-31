from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from static import GeoList, GenreList, CinemaList, TipologiaList
from multiselectfield import MultiSelectField
from datetime import datetime
from . import validators


class Invito(models.Model):
    tipologia = models.CharField(max_length=100, choices=TipologiaList.TipologiaList.ListaTipologia, default="Cinema")
    cinema = models.CharField(max_length=100, blank=True)
    film = models.CharField(max_length=100)
    data = models.DateField(validators=[validators.validate_date])
    orario = models.TimeField()
    limite_persone = models.PositiveSmallIntegerField()
    genere = MultiSelectField(max_length=100, choices=GenreList.GenreList.ListaGeneri)

    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    commento = models.TextField(blank=True)
    data_invito = models.DateTimeField(default=timezone.now)

    partecipanti = models.ManyToManyField(User, related_name='partecipanti', blank=True)

    @property
    def posti_rimasti(self):
        return self.limite_persone - self.partecipanti.count()

    @property
    def scaduto(self):
        return self.data < datetime.today().date()

    class Meta:
        verbose_name = 'Invito'
        verbose_name_plural = "Inviti"

    def __str__(self):
        return self.film

    def get_absolute_url(self):
        return reverse('invito-detail', kwargs={'pk': self.pk})
