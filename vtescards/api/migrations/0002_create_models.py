# Generated by Django 3.1.6 on 2021-03-23 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_trigram_extension'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('aka', models.CharField(max_length=64, null=True)),
                ('alias', models.CharField(max_length=64)),
                ('card_type', models.CharField(max_length=32)),
                ('publish_set', models.CharField(max_length=256)),
                ('banned', models.IntegerField(null=True)),
                ('artist', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('abbreviation', models.CharField(max_length=16)),
                ('release_date', models.DateField(null=True)),
                ('company', models.CharField(max_length=32, null=True)),
                ('icon', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CryptCard',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.card')),
                ('clan', models.CharField(max_length=32)),
                ('advanced', models.BooleanField(default=False)),
                ('group_id', models.CharField(max_length=8)),
                ('capacity', models.IntegerField()),
                ('disciplines', models.CharField(max_length=128)),
                ('card_text', models.CharField(max_length=1024)),
                ('title', models.CharField(max_length=128, null=True)),
                ('abombwe', models.IntegerField(default=0)),
                ('animalism', models.IntegerField(default=0)),
                ('auspex', models.IntegerField(default=0)),
                ('celerity', models.IntegerField(default=0)),
                ('chimerstry', models.IntegerField(default=0)),
                ('daimoinon', models.IntegerField(default=0)),
                ('dementation', models.IntegerField(default=0)),
                ('dominate', models.IntegerField(default=0)),
                ('fortitude', models.IntegerField(default=0)),
                ('melpominee', models.IntegerField(default=0)),
                ('mytherceria', models.IntegerField(default=0)),
                ('necromancy', models.IntegerField(default=0)),
                ('obeah', models.IntegerField(default=0)),
                ('obfuscate', models.IntegerField(default=0)),
                ('obtenebration', models.IntegerField(default=0)),
                ('potence', models.IntegerField(default=0)),
                ('presence', models.IntegerField(default=0)),
                ('protean', models.IntegerField(default=0)),
                ('quietus', models.IntegerField(default=0)),
                ('sanguinus', models.IntegerField(default=0)),
                ('serpentis', models.IntegerField(default=0)),
                ('spiritus', models.IntegerField(default=0)),
                ('temporis', models.IntegerField(default=0)),
                ('thanatosis', models.IntegerField(default=0)),
                ('thaumaturgy', models.IntegerField(default=0)),
                ('valeren', models.IntegerField(default=0)),
                ('vicissitude', models.IntegerField(default=0)),
                ('visceratika', models.IntegerField(default=0)),
            ],
            bases=('api.card',),
        ),
        migrations.CreateModel(
            name='LibraryCard',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.card')),
                ('clan', models.CharField(max_length=32, null=True)),
                ('discipline', models.CharField(max_length=64, null=True)),
                ('pool_cost', models.CharField(max_length=2, null=True)),
                ('blood_cost', models.CharField(max_length=2, null=True)),
                ('conviction_cost', models.CharField(max_length=2, null=True)),
                ('burn_option', models.BooleanField(default=False)),
                ('card_text', models.CharField(max_length=1024)),
                ('flavor_text', models.CharField(max_length=512, null=True)),
                ('requirement', models.CharField(max_length=128, null=True)),
                ('capacity', models.CharField(max_length=32, null=True)),
                ('draft', models.CharField(max_length=256, null=True)),
            ],
            bases=('api.card',),
        ),
        migrations.CreateModel(
            name='CardSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=32, null=True)),
                ('image', models.CharField(max_length=128, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.card')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.set')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='publish_sets',
            field=models.ManyToManyField(blank=True, through='api.CardSet', to='api.Set'),
        ),
    ]