# Generated by Django 3.1.13 on 2022-08-29 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_load_set_icons'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='set',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='card',
            name='publish_set',
            field=models.CharField(max_length=512),
        ),
    ]
