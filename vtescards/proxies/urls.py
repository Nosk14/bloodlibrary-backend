from django.urls import path, include
from proxies.views import generate_pdf, download_pdf


urlpatterns = [
    path('generate', generate_pdf),
    path('download/<str:id>', download_pdf)
]
