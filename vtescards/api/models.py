from django.db import models

class Card:
    id = models.CharField(max_length=16, blank=False)
    name = models.CharField(max_length=32, blank=False)
    aka = models.CharField(max_length=32)
    card_type = models.CharField(max_length=32, blank=False)

    @property
    def image(self):
        return f'https://vtes.dirtydevelopers.org/img/{self.id}.jpg'

class LibraryCard(Card, models.Model):
    pass

class CryptCard(Card, models.Model):
    pass