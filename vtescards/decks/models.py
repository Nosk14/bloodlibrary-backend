from django.db import models


class TournamentDeck(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    author = models.CharField(max_length=128, blank=True, null=True)
    vekn_id = models.CharField(max_length=64, blank=False, null=False)
    vtesdecks_id = models.CharField(max_length=64, blank=False, null=False, unique=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    num_players = models.IntegerField(null=False)
    year = models.IntegerField(null=True)
    vtesdecks_link = models.CharField(max_length=128, blank=False, null=False, unique=True)

    def __str__(self):
        return f"[{self.vekn_id}] {self.name}"
