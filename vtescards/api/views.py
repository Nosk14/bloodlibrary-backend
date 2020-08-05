from rest_framework.exceptions import APIException
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import redirect
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
        if not name_param or len(name_param) < 2:
            raise APIException(code=400, detail="Parameter 'name' must be specified with a length greater than 1.")

        return Card.objects \
            .annotate(similarity=TrigramSimilarity('alias', name_param)) \
            .filter(similarity__gt=0.20) \
            .order_by('-similarity')


def get_card_image(request):
    name_param = request.GET.get('name', None)
    if not name_param or len(name_param) < 2:
        raise APIException(code=400, detail="Parameter 'name' must be specified with a length greater than 2.")

    name_param = name_param.lower()
    cards = Card.objects \
        .annotate(similarity=TrigramSimilarity('alias', name_param)) \
        .filter(similarity__gt=0.20) \
        .order_by('-similarity')

    if not cards:
        raise APIException(code=404, detail="No cards found")

    img_link = f'https://vtes.dirtydevelopers.org/img/{cards[0].id}.jpg'
    return redirect(img_link)
