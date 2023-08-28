from django.urls import path, include
from rest_framework.routers import DefaultRouter

from decks.views import RandomTournamentDeckView

router = DefaultRouter()
router.register('random', RandomTournamentDeckView, basename='random-deck')

urlpatterns = [
    path('', include(router.urls)),
]
