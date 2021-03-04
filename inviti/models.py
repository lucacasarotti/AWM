from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from static import GenreList


class Invito (models.Model):
    class Meta:
        verbose_name_plural = "Inviti"

    CINEMA_CHOICES = [
        ('VC', 'Victoria Cinema'),
        ('CR', 'Cinema Raffaello'),
        ('CA', 'Cinema Astra'),
    ]
    GENERE_CHOICES=[('Commedia', 'Commedia'), ('Fantascienza', 'Fantascienza'),
     ('Horror', 'Horror'), ('Romantico', 'Romantico'), ('Azione', 'Azione'),
     ('Thriller', 'Thriller'), ('Drammatico', 'Drammatico'), ('Mistero', 'Mistero'),
     ('Giallo', 'Giallo'), ('Animazione', 'Animazione'), ('Avventura', 'Avventura'),
     ('Fantasy', 'Fantasy'), ('Commedia romantica', 'Commedia romantica'),
     ('Commedia d\'azione', 'Commedia d\'azione'), ('Supereroi', 'Supereroi'),
     ('Storico', 'Storico'), ('Biografico', 'Biografico'), ('Documentario', 'Documentario'),
     ('Musical', 'Musical'), ('Guerra', 'Guerra'), ('Western', 'Western'),]

    cinema = models.CharField(max_length=100, choices=CINEMA_CHOICES)

    film = models.CharField(max_length=100)
    data = models.DateField()
    orario = models.TimeField()
    limite_persone = models.PositiveSmallIntegerField()
    genere = models.CharField(max_length=100, choices=GENERE_CHOICES)

    # citta = models.CharField(max_length=100)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    commento = models.TextField()
    data_invito = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.film
