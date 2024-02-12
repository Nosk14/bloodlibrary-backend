from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Card
from pod.serializers import CardWithShopSerializer


class CardShopViewSet(ReadOnlyModelViewSet):
    queryset = Card.objects.prefetch_related('shops').filter(shops__isnull=False)
    serializer_class = CardWithShopSerializer
