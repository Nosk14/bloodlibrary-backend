# Generated by Django 3.0.7 on 2020-08-04 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_card_cryptcard_librarycard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expansion',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('abbreviation', models.CharField(max_length=16)),
                ('release_date', models.DateField(null=True)),
                ('icon', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentDeck',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, null=True)),
                ('event', models.CharField(max_length=64, null=True)),
                ('player', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('event_date', models.DateField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='alias',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
    ]
