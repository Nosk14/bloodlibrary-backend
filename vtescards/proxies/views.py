from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotFound, FileResponse
from proxies.utils import ProxyFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import Counter
import json

IMG_TEMPLATE = "https://statics.bloodlibrary.info/img/proxy/{0}.jpg"

generated_pdfs = Counter("bloodlibrary_generated_pdfs", "Amount of successful calls to PDF generation endpoint.")
single_card_counter = Counter("bloodlibrary_single_card_proxies", "Amount of times a single card has been printed as a proxy.", ['card_id'])

@csrf_exempt
@require_http_methods(['POST'])
def generate_pdf(request):
    text = request.body.decode('utf-8')
    data = json.loads(text)
    if not data:
        return HttpResponseBadRequest()

    proxy_file = ProxyFile()
    for card in data:
        for _ in range(card['amount']):
            proxy_file.add_image(IMG_TEMPLATE.format(card['id']))

    proxy_file.save()

    generated_pdfs.inc()
    for card in data:
        single_card_counter.labels(card_id=card['id']).inc(card['amount'])

    return FileResponse(proxy_file.serve_buffer(), as_attachment=True, filename='vtes_proxies.pdf')
