from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from api.models import Card, CryptCard, LibraryCard, CardSet, Set


class SetCardListSerializer(ModelSerializer):
    id = ReadOnlyField(source='card.id')
    name = ReadOnlyField(source='card.name')

    class Meta:
        model = CardSet
        fields = ('id', 'name', 'image')


class CardExpansionSerializer(ModelSerializer):
    set_name = ReadOnlyField(source='set.name')
    set_abbreviation = ReadOnlyField(source='set.abbreviation')

    class Meta:
        model = CardSet
        fields = ('set_name', 'set_abbreviation', 'info', 'image')


class SetSerializer(ModelSerializer):
    cards = SetCardListSerializer(source='cardset_set', read_only=True, many=True, required=False)

    class Meta:
        model = Set
        fields = ('id', 'name', 'abbreviation', 'release_date', 'company', 'icon', 'cards')


class CardSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')
    publish_sets = CardExpansionSerializer(source='cardset_set', read_only=True, many=True, required=False)

    @staticmethod
    def get_image(obj):
        return f'https://statics.bloodlibrary.info/img/all/{obj.id}.jpg'

    class Meta:
        model = Card
        fields = ('id', 'name', 'aka', 'alias', 'card_type', 'banned', 'artist', 'image', 'publish_sets')


class CryptCardSerializer(CardSerializer):
    class Meta:
        model = CryptCard
        fields = '__all__'


class LibraryCardSerializer(CardSerializer):
    class Meta:
        model = LibraryCard
        fields = '__all__'
