from api.models import CardSet, Set, Card
from django.db import migrations


def add_tokens(apps, schema_editor):
    custom_set = Set.objects.get(id='399997')
    LibraryCard = apps.get_model('api', 'LibraryCard')

    LibraryCard(id='199999',
                name="Khazar's Diary Wraith (Token)",
                alias="Khazar's Diary Wraith (Token)",
                card_type="Ally"
                ).save()

    CardSet(card=Card.objects.get(pk='199999'),
            set=custom_set,
            image="https://statics.bloodlibrary.info/img/sets/custom/KhazarWraith.png"
            ).save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0006_auto_20220904_1514'),
    ]

    operations = [
        migrations.RunPython(add_tokens)
    ]
