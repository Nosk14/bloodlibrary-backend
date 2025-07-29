from django.db import migrations

from api.models import CardSet, Set, Card


def add_tokens(apps, schema_editor):
    custom_set = Set.objects.get(id='399997')
    LibraryCard = apps.get_model('api', 'LibraryCard')
    CryptCard = apps.get_model('api', 'CryptCard')

    LibraryCard(id='199999',
                name="Khazar's Diary Wraith (Token)",
                alias="Khazar's Diary Wraith (Token)",
                card_type="Ally"
                ).save()

    CardSet(card=Card.objects.get(pk='199999'),
            set=custom_set,
            image="https://statics.bloodlibrary.info/img/sets/custom/KhazarWraith.png"
            ).save()

    CryptCard(id='299999',
              name="The Great Beast (FOR, OBE, DAI) (Token)",
              alias="The Great Beast (FOR, OBE, DAI) (Token)",
              capacity=9
              ).save()

    CardSet(card=Card.objects.get(pk='299999'),
            set=custom_set,
            image="https://statics.bloodlibrary.info/img/sets/custom/TheGreatBeast_FOROBDAI.png"
            ).save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0006_auto_20220904_1514'),
    ]

    operations = [
         migrations.RunPython(add_tokens)
    ]
