from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CardViewSet, CryptCardViewSet, LibraryCardViewSet, CardSearchViewSet

router = DefaultRouter()
router.register('cards', CardViewSet)
router.register('search', CardSearchViewSet, basename='cards-search')
router.register('crypt', CryptCardViewSet)
router.register('library', LibraryCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

