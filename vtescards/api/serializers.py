from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from api.models import Card, CryptCard, LibraryCard, CardSet, Set


class SetSerializer(ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'


class CardExpansionSerializer(ModelSerializer):
    set_name = ReadOnlyField(source='set.name')
    set_abbreviation = ReadOnlyField(source='set.abbreviation')

    class Meta:
        model = CardSet
        fields = ('set_name', 'set_abbreviation', 'info', 'image')


class CardSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')
    publish_sets = CardExpansionSerializer(source='cardset_set', read_only=True, many=True, required=False)

    @staticmethod
    def get_image(obj):
        return f'https://statics.bloodlibrary.info/img/all/{obj.id}.jpg'

    class Meta:
        model = Card
        exclude = ('publish_set', )


class CryptCardSerializer(CardSerializer):
    class Meta:
        model = CryptCard
        fields = '__all__'


class LibraryCardSerializer(CardSerializer):
    class Meta:
        model = LibraryCard
        fields = '__all__'
