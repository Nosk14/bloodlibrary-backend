from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CardViewSet, CryptCardViewSet, LibraryCardViewSet

router = DefaultRouter()
router.register('cards', CardViewSet)
router.register('crypt', CryptCardViewSet)
router.register('library', LibraryCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

