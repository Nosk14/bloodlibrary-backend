from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotFound, FileResponse
from proxies.utils import ProxyFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import Counter
from api.models import CardSet
import json

generated_pdfs = Counter("bloodlibrary_generated_pdfs", "Amount of successful calls to PDF generation endpoint.")
single_card_counter = Counter("bloodlibrary_single_card_proxies", "Amount of times a single card has been printed as a proxy.", ['card_id'])


@csrf_exempt
@require_http_methods(['POST'])
def generate_pdf(request):
    text = request.body.decode('utf-8')
    rq_data = json.loads(text)
    if not rq_data:
        return HttpResponseBadRequest()

    cards = rq_data['cards']
    line_color = rq_data.get('lineColor', "#FFFFFF")
    proxy_file = ProxyFile(line_color=line_color)

    for card in cards:
        if 'set' in card and card['set']:
            result = CardSet.objects \
                .filter(card_id=card['id'], set_id=card['set']) \
                .exclude(image=None)
            result = list(result)

            if not result:
                return HttpResponseBadRequest()

            card_image = result[0].image
        else:
            card_image = CardSet.objects\
                .filter(card_id=card['id'])\
                .exclude(image=None)\
                .order_by('-set_id')[0].image

        for _ in range(card['amount']):
            proxy_file.add_image(card_image)

    proxy_file.save()

    generated_pdfs.inc()
    for card in cards:
        single_card_counter.labels(card_id=card['id']).inc(card['amount'])

    return FileResponse(proxy_file.serve_buffer(), as_attachment=True, filename='vtes_proxies.pdf')

