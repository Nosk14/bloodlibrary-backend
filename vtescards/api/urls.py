from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CardViewSet, CryptCardViewSet, LibraryCardViewSet, CardSearchViewSet, get_card_image, SetViewSet

router = DefaultRouter()
router.register('cards', CardViewSet)
router.register('search', CardSearchViewSet, basename='cards-search')
router.register('crypt', CryptCardViewSet)
router.register('library', LibraryCardViewSet)
router.register('sets', SetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('image', get_card_image)
]

