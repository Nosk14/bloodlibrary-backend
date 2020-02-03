from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CardViewSet

router = DefaultRouter()
router.register('cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

