from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import Card, CryptCard, LibraryCard


class CardSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')

    @staticmethod
    def get_image(self):
        return f'https://vtes.dirtydevelopers.org/img/{self.id}.jpg'

    class Meta:
        model = Card
        fields = '__all__'


class CryptCardSerializer(CardSerializer):

    class Meta:
        model = CryptCard
        fields = '__all__'


class LibraryCardSerializer(CardSerializer):

    class Meta:
        model = LibraryCard
        fields = '__all__'