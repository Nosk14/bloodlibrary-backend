from django.core.management.base import BaseCommand, CommandError
import csv
from importlib.resources import open_text
from api.models import CardSet, Set, Card, LibraryCard, CryptCard
from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests
from django.db.models import Q


PACKAGE = 'api.data'


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Loading expansions...")
        load_expansions()
        self.stdout.write("Loading library...")
        # load_library()
        self.stdout.write("Loading crypt...")
        load_crypt()
        self.stdout.write("Loading images...")
        update_all_images()
        self.stdout.write("Loading icons...")
        update_all_icon_images()
        self.stdout.write("Done!")


def _load_card_expansions(card_id, raw_expansions_field):
    if raw_expansions_field:
        expansions = raw_expansions_field.split(',')
        for expansion in expansions:
            exp = expansion.strip()
            expansion_data = exp.split(':')
            expansion_id = expansion_data[0].strip()
            print(expansion_id)
            info = None if len(expansion_data) < 2 else expansion_data[1].strip()
            set_obj = Set.objects.get(abbreviation=expansion_id)
            card_obj = Card.objects.get(pk=card_id)
            CardSet(card=card_obj, set=set_obj, info=info, image=None).save()


def load_library():
    with open_text(PACKAGE, 'vteslib.csv', encoding='utf8') as csv_library:
        next(csv_library)
        reader = csv.reader(csv_library, delimiter=',')
        for row in reader:
            lc = LibraryCard(
                id=row[0],
                name=row[1],
                aka=row[2] if row[2] else None,
                alias=row[1],
                card_type=row[3],
                clan=row[4],
                discipline=row[5] if row[5] else None,
                pool_cost=row[6] if row[6] else "0",
                blood_cost=row[7] if row[7] else "0",
                conviction_cost=row[8] if row[8] else "0",
                burn_option=bool(row[9]),
                card_text=row[10],
                flavor_text=row[11] if row[11] else None,
                publish_set=row[12] if row[12] else None,
                requirement=None,
                banned=int(row[13]) if row[13] else None,
                artist=row[14],
                capacity=row[15] if row[15] else None,
                draft=None,
             )
            lc.save()
            _load_card_expansions(row[0], row[12])


def load_crypt():
    with open_text(PACKAGE, 'vtescrypt.csv', encoding='utf8') as csv_crypt:
        next(csv_crypt)
        reader = csv.reader(csv_crypt, delimiter=',')
        crypt_cards = [
            CryptCard(id=row[0],
                      name=row[1],
                      aka=row[2] if row[2] else None,
                      alias=row[1] if not bool(row[5]) else row[1] + " (ADV)",
                      card_type=row[3],
                      clan=row[4],
                      advanced=bool(row[5]),
                      group_id=row[6],
                      capacity=int(row[7]),
                      disciplines=row[8],
                      card_text=row[9],
                      publish_set=row[10],
                      title=row[11] if row[11] else None,
                      banned=int(row[12]) if row[12] else None,
                      artist=row[13]
                      )
            for row in reader
        ]
        crypt_cards.sort(key=lambda card: card.id)
        used_aliases = set()
        for cc in crypt_cards:
            print(cc.name)
            if not cc.advanced:
                if cc.alias in used_aliases:
                    cc.alias = f"{cc.alias} (G{cc.group_id})"
                else:
                    used_aliases.add(cc.alias)
            cc.save()
            _load_card_expansions(cc.id, cc.publish_set)  # id - publish_set


def load_expansions():
    with open_text(PACKAGE, 'vtessets.csv', encoding='utf8') as csv_sets:
        next(csv_sets)
        reader = csv.reader(csv_sets, delimiter=',')
        for row in reader:
            expansion = Set(
                id=row[0],
                abbreviation=row[1],
                release_date=datetime.strptime(row[2], '%Y%m%d').date(),
                name=row[3],
                company=row[4],
                icon=None
            )
            expansion.save()

    Set(id='399999',
        abbreviation='POD',
        name='Print on Demand'
        ).save()
    Set(id='399997',
        abbreviation='CUSTOM',
        name='CUSTOM'
        ).save()


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


def update_all_images():
    #cardsets = list(CardSet.objects.all())
    cardsets = list(CardSet.objects.filter(Q(image__isnull=True) | Q(image='')))
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


def check_icon_image(set_id):
    img_url = 'https://statics.bloodlibrary.info/img/icons/{0}.gif'.format(set_id)
    rs = requests.head(img_url)
    if rs.status_code == 200:
        return set_id, img_url
    else:
        return None


def update_all_icon_images():
    sets = list(Set.objects.all())
    parsed_sets = [zet.id for zet in sets]

    pool = ThreadPool(processes=16)
    results = pool.map(check_icon_image, parsed_sets)
    pool.close()
    pool.join()

    indexed_objects = {cs.id: cs for cs in sets}
    objects_to_update = []
    for result in results:
        if result:
            zet = indexed_objects[result[0]]
            zet.icon = result[1]
            objects_to_update.append(zet)
    Set.objects.bulk_update(objects_to_update, ['icon'])
