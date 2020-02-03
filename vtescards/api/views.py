from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import Card
from api.serializers import CardSerializer


class CardViewSet(ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CardSerializer




