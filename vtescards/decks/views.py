from rest_framework.viewsets import ReadOnlyModelViewSet
from decks.serializers import TournamentDeckSerializer
from decks.models import TournamentDeck
import random


class RandomTournamentDeckView(ReadOnlyModelViewSet):
    serializer_class = TournamentDeckSerializer

    def get_queryset(self):
        q = TournamentDeck.objects

        country_filter = self.request.query_params.get('country', None)
        if country_filter:
            q = q.filter(country=country_filter)

        objects = list(q.all())

        return [random.choice(objects)]
