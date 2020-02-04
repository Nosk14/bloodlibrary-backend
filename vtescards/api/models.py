from django.db import models


class Card(models.Model):
    id = models.CharField(max_length=16, blank=False, primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    aka = models.CharField(max_length=64)
    card_type = models.CharField(max_length=32, blank=False)


class LibraryCard(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE, primary_key=True)
    clan = models.CharField(max_length=32)
    discipline = models.CharField(max_length=64)


class CryptCard(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE, primary_key=True)
    clan = models.CharField(max_length=32)
    advanced = models.BooleanField(default=False)

