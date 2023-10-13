import csv
from importlib.resources import open_text
from api.models import CardSet, Set, Card
from django.db import migrations
from datetime import datetime


PACKAGE = 'api.data'


def load_card_expansions(card_id, raw_expansions_field):
    if raw_expansions_field:
        expansions = raw_expansions_field.split(',')
        for expansion in expansions:
            exp = expansion.strip()
            expansion_data = exp.split(':')
            expansion_id = expansion_data[0].strip()
            info = expansion_data[1].strip() if len(expansion_data) > 0 else None
            set_obj = Set.objects.get(abbreviation=expansion_id)
            card_obj = Card.objects.get(pk=card_id)
            CardSet(card=card_obj, set=set_obj, info=info, image=None).save()


def load_library(apps, schema_editor):
    LibraryCard = apps.get_model('api', 'LibraryCard')
    with open_text(PACKAGE, 'vteslib.csv', encoding='utf8') as csv_library:
        next(csv_library)
        reader = csv.reader(csv_library, delimiter=',')
        for row in reader:
            lc = LibraryCard(id=row[0],
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

            load_card_expansions(row[0], row[12])


def load_crypt(apps, schema_editor):
    CryptCard = apps.get_model('api', 'CryptCard')
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
            if not cc.advanced:
                if cc.alias in used_aliases:
                    cc.alias = f"{cc.alias} (G{cc.group_id})"
                else:
                    used_aliases.add(cc.alias)
            cc.save()
            load_card_expansions(cc.id, cc.publish_set)  # id - publish_set


def load_expansions(apps, schema_editor):
    with open_text(PACKAGE, 'vtessets.csv', encoding='utf8') as csv_sets:
        next(csv_sets)
        reader = csv.reader(csv_sets, delimiter=',')
        for row in reader:
            expansion = Set(id=row[0],
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


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_create_models')
    ]

    operations = [
        migrations.RunPython(load_expansions),
        migrations.RunPython(load_library),
        migrations.RunPython(load_crypt),
    ]
