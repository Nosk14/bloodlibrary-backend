from django.db import models


class Set(models.Model):
    id = models.CharField(max_length=16, null=False, primary_key=True)
    name = models.CharField(max_length=64, null=False)
    abbreviation = models.CharField(max_length=16, null=False)
    release_date = models.DateField(null=True)
    company = models.CharField(max_length=64, null=True)
    icon = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"Set({self.id}, {self.name}, {self.abbreviation})"

    class Meta:
        ordering = ['id']


class Card(models.Model):
    id = models.CharField(max_length=16, null=False, primary_key=True)
    name = models.CharField(max_length=64, null=False)
    aka = models.CharField(max_length=64, null=True)
    alias = models.CharField(max_length=64, null=False)
    card_type = models.CharField(max_length=64, null=False)
    publish_set = models.CharField(max_length=512)
    banned = models.IntegerField(null=True)
    artist = models.CharField(max_length=128)
    publish_sets = models.ManyToManyField(Set, through='CardSet', blank=True)

    def __str__(self):
        return f"Card({self.id}, {self.alias})"


class LibraryCard(Card):
    clan = models.CharField(max_length=64, null=True)
    discipline = models.CharField(max_length=64, null=True)
    pool_cost = models.CharField(max_length=2, null=True)
    blood_cost = models.CharField(max_length=2, null=True)
    conviction_cost = models.CharField(max_length=2, null=True)
    burn_option = models.BooleanField(default=False)
    card_text = models.CharField(max_length=1024)
    flavor_text = models.CharField(max_length=512, null=True)
    requirement = models.CharField(max_length=128, null=True)
    capacity = models.CharField(max_length=64, null=True)
    draft = models.CharField(max_length=256, null=True)


class CryptCard(Card):
    clan = models.CharField(max_length=64)
    advanced = models.BooleanField(default=False)
    group_id = models.CharField(max_length=8)
    capacity = models.IntegerField()
    disciplines = models.CharField(max_length=128)
    card_text = models.CharField(max_length=1024)
    title = models.CharField(max_length=128, null=True)


class CardSet(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    info = models.CharField(max_length=64, null=True)
    image = models.CharField(max_length=128, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['card', 'set', 'info', 'image'], name="unique_cardset"),
        ]

    def __str__(self):
        return f"CardSet({self.card.alias}, {self.set.abbreviation})"


class PrivateCard(models.Model):
    id = models.CharField(max_length=16, null=False, primary_key=True)
    name = models.CharField(max_length=64, null=False)
    alias = models.CharField(max_length=64, null=False)
