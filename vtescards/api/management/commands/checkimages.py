from django.core.management.base import BaseCommand, CommandError
import csv
from importlib.resources import open_text

from django.db import IntegrityError

from api.models import CardSet, Set, Card, LibraryCard, CryptCard
from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests
from django.db.models import Q


PACKAGE = 'api.data'


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Loading images...")
        self.update_all_images()
        self.stdout.write("Done!")

    def check_image(self, cardset_id, set_abbreviation, card_id):
        if set_abbreviation.lower().startswith('promo-'):
            set_abbreviation = 'promo'
        card_set_img = 'https://statics.bloodlibrary.info/img/sets/{0}/{1}.jpg'.format(set_abbreviation.lower(), card_id)
        rs = requests.head(card_set_img)
        if rs.status_code == 200:
            return card_set_img
        else:
            return None

    def update_all_images(self):
        for cardset in CardSet.objects.filter(Q(image__isnull=True) | Q(image='')).iterator(chunk_size=250):
            img_link = self.check_image(cardset.id, cardset.set.abbreviation, cardset.card_id)
            if img_link:
                cardset.image = img_link
                cardset.save()
