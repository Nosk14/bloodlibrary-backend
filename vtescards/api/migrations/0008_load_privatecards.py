# Generated by Django 3.1.13 on 2022-12-23 11:24

from django.db import migrations
import os
import json


def load_private_cards(apps, schema_editor):
    PrivateCard = apps.get_model('api', 'PrivateCard')
    raw_cards = os.getenv('PRIVATE_CARDS', None)
    if raw_cards:
        single_raws = raw_cards.split('@')
        for card in single_raws:
            id, name, alias = card.split('#')
            PrivateCard(id=id, name=name, alias=alias).save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_privatecard'),
    ]

    operations = [
          # migrations.RunPython(load_private_cards)
    ]
