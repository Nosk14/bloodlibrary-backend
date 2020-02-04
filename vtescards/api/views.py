from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import Card, CryptCard, LibraryCard
from api.serializers import CardSerializer, CryptCardSerializer, LibraryCardSerializer


class CardViewSet(ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CardSerializer


class CryptCardViewSet(ReadOnlyModelViewSet):
    queryset = CryptCard.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CryptCardSerializer


class LibraryCardViewSet(ReadOnlyModelViewSet):
    queryset = LibraryCard.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = LibraryCardSerializer