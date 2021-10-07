from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotFound, FileResponse
from proxies.utils import ProxyFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

IMG_TEMPALTE = "https://statics.bloodlibrary.info/img/proxy/{0}.jpg"


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
            proxy_file.add_image(IMG_TEMPALTE.format(card['id']))

    proxy_file.save()

    return FileResponse(proxy_file.serve_buffer(), as_attachment=True, filename='vtes_proxies.pdf')
