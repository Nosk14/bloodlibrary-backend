from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, Http404, FileResponse
from django.contrib.postgres.search import TrigramSimilarity
from api.models import Card, CryptCard
from proxies.utils import ProxyFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import uuid

STORE_LOCATION = '/tmp/'


@csrf_exempt
@require_http_methods(['POST'])
def generate_pdf(request):
    text = request.body.decode('utf-8')
    if text is None:
        return HttpResponseBadRequest()

    raw_data = text.strip()
    if not raw_data:
        return HttpResponseBadRequest()

    cards = []
    for line in raw_data.splitlines():
        striped_line = line.strip()
        if striped_line:
            num, name = striped_line.split(maxsplit=1)
            cards.append((num, name))

    proxy_list = []
    for card in cards:
        similar_cards = __get_similar_cards(card[1])
        if similar_cards:
            card_id = similar_cards[0].id
            image_url = "https://bloodlibrary.info/img/proxy/" + card_id + ".jpg"
            proxy_list.append((int(card[0]), image_url))

    if not proxy_list:
        return HttpResponse(status=204)

    file_id = str(uuid.uuid1())
    proxy_file = ProxyFile(STORE_LOCATION + file_id)
    for proxy in proxy_list:
        for _ in range(proxy[0]):
            proxy_file.add_image(proxy[1])

    proxy_file.save()

    return JsonResponse({'id': file_id})


def __get_similar_cards(name):
    return Card.objects \
            .annotate(similarity=TrigramSimilarity('name', name)) \
            .filter(similarity__gt=0.20) \
            .order_by('-similarity')


@require_http_methods(['GET'])
def download_pdf(request, id):
    try:
        file = open(STORE_LOCATION + id + ".pdf", 'rb')
        return FileResponse(file, as_attachment=True, filename='vtes_proxies.pdf')
    except FileNotFoundError:
        return Http404()
