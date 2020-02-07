from rest_framework.exceptions import APIException
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.postgres.search import TrigramSimilarity
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


class CardSearchViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CardSerializer

    def get_queryset(self):
        name_param = self.request.query_params.get('name', None)
        if not name_param or len(name_param) < 3:
            raise APIException(code=400, detail="Parameter 'name' must be specified with a length greater than 2.")

        return Card.objects \
            .annotate(similarity=TrigramSimilarity('name', name_param)) \
            .filter(similarity__gt=0.20) \
            .order_by('-similarity')
