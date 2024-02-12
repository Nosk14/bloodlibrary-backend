from django.db import models
from api.models import Card


class CardShop(models.Model):
    card = models.ForeignKey(Card, related_name='shops', on_delete=models.CASCADE)
    shop = models.TextField(max_length=128)
    link = models.TextField(max_length=512)
    release_date = models.DateField()

    class Meta:
        unique_together = ('card', 'shop',)
        ordering = ('shop', )
