from django.contrib.auth.models import User
from django.db import models


class Recensione(models.Model):
    user_recensore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recensore')
    user_recensito = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recensito')
    titolo = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=250)
    voto = models.IntegerField(default=1)
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recensione'
        verbose_name_plural = "Recensioni"
        ordering = ['-timestamp']

    def __str__(self):
        return self.titolo