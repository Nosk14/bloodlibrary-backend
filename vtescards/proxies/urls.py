from django.urls import path, include
from proxies.views import generate_pdf


urlpatterns = [
    path('generate', generate_pdf),
]
