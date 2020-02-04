from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import Card


class CardSerializer(ModelSerializer):
    image = SerializerMethodField('get_image')

    @staticmethod
    def get_image(self):
        return f'https://vtes.dirtydevelopers.org/img/{self.id}.jpg'

    class Meta:
        model = Card
        fields = '__all__'
