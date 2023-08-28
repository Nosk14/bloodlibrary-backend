from rest_framework.serializers import ModelSerializer
from decks.models import TournamentDeck


class TournamentDeckSerializer(ModelSerializer):

    class Meta:
        model = TournamentDeck
        fields = '__all__'
