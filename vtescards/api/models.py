from django.db import models


class Card(models.Model):
    id = models.CharField(max_length=16, blank=False, primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    aka = models.CharField(max_length=64)
    card_type = models.CharField(max_length=32, blank=False)


class LibraryCard(Card):
    clan = models.CharField(max_length=32)
    discipline = models.CharField(max_length=64)


class CryptCard(Card):
    clan = models.CharField(max_length=32)
    advanced = models.BooleanField(default=False)

