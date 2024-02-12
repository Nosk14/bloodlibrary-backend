from django.urls import path
from pod.views import CardShopViewSet


urlpatterns = [
    path('cards', CardShopViewSet.as_view({'get': 'list'})),
]
