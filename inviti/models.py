from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from static import GeoList, GenreList, CinemaList


class Invito(models.Model):

    cinema = models.CharField(max_length=100, choices=CinemaList.CinemaList.ListaCinema)
    film = models.CharField(max_length=100)
    data = models.DateField()
    orario = models.TimeField()
    limite_persone = models.PositiveSmallIntegerField()
    posti_rimanenti = models.PositiveSmallIntegerField(default=1)
    genere = models.CharField(max_length=100, choices=GenreList.GenreList.ListaGeneri)

    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    commento = models.TextField()
    data_invito = models.DateTimeField(default=timezone.now)

    # partecipanti = models.CharField(max_length=100, default="")
    partecipanti = models.ManyToManyField(User, related_name='partecipanti', blank=True)

    class Meta:
        verbose_name = 'Invito'
        verbose_name_plural = "Inviti"

    def __str__(self):
        return self.film

    def get_absolute_url(self):
        return reverse('invito-detail', kwargs={'pk': self.pk})
