from django.db.models import Subquery
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Card
from pod.models import CardShop
from pod.serializers import CardWithShopSerializer


class CardShopViewSet(ReadOnlyModelViewSet):
    queryset = Card.objects.filter(id__in=Subquery(CardShop.objects.values_list('card_id', flat=True)))
    serializer_class = CardWithShopSerializer
