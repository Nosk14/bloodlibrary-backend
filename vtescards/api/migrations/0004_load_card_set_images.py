# Generated by Django 3.1.6 on 2021-03-23 16:09

from django.db import migrations
from multiprocessing.pool import ThreadPool
import requests


def check_image(card_set):
    cardset_id, set_abbreviation, card_id = card_set
    if set_abbreviation.lower().startswith('promo-'):
        set_abbreviation = 'promo'
    card_set_img = 'https://statics.bloodlibrary.info/img/sets/{0}/{1}.jpg'.format(set_abbreviation.lower(), card_id)
    rs = requests.head(card_set_img)
    if rs.status_code == 200:
        return cardset_id, card_set_img
    else:
        return None


def update_all_images(apps, schema_editor):
    CardSet = apps.get_model('api', 'CardSet')
    cardsets = list(CardSet.objects.all())
    parsed_cardsets = [(cardset.id, cardset.set.abbreviation, cardset.card.id) for cardset in cardsets]

    pool = ThreadPool(processes=16)
    results = pool.map(check_image, parsed_cardsets)
    pool.close()
    pool.join()

    indexed_objects = {cs.id: cs for cs in cardsets}
    objects_to_update = []
    for result in results:
        if result:
            cardset = indexed_objects[result[0]]
            cardset.image = result[1]
            objects_to_update.append(cardset)
    CardSet.objects.bulk_update(objects_to_update, ['image'])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0003_load_data'),
    ]

    operations = [
        # migrations.RunPython(update_all_images)
    ]
