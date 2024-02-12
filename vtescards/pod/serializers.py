from rest_framework import serializers

from api.models import Card
from pod.models import CardShop


class CardShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardShop
        fields = ['shop', 'link', 'release_date']


class CardWithShopSerializer(serializers.ModelSerializer):
    shops = CardShopSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'name', 'alias', 'card_type', 'shops']


