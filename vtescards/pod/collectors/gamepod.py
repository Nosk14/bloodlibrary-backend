import requests
import datetime

from django.contrib.postgres.search import TrigramSimilarity

from api.models import Card
from pod.models import CardShop


class GamepodCollector:
    PRODUCTS_ENDPOINT = "https://www.gamepod.es/products.json?limit=250&page="
    URL_TEMPLATE = "https://www.gamepod.es/products/{0}"

    def collect_cards(self):
        products = self.__get_products_info()
        parsed_products = [
            {
                'name': p['title'].rsplit("-", 1)[0],
                'link': GamepodCollector.URL_TEMPLATE.format(p['handle']),
                'release_date': datetime.datetime.strptime(p['published_at'].split('T')[0], "%Y-%m-%d").date()
            } for p in products
        ]
        self.__parse_cards(parsed_products)

    def __get_products_info(self):
        result = []
        page = 1
        products = requests.get(GamepodCollector.PRODUCTS_ENDPOINT + str(page)).json()['products']
        result.extend(products)
        page += 1
        while len(products) > 0:
            products = requests.get(GamepodCollector.PRODUCTS_ENDPOINT + str(page)).json()['products']
            result.extend(products)
            page += 1

        return list(filter(lambda x: x["product_type"] == "Cartas", result))

    def __parse_cards(self, parsed_products):
        for product in parsed_products:
            card = self.__identify_card(product['name'])
            CardShop.objects.update_or_create(
                card=card,
                shop="Gamepod",
                defaults={
                    "link": product['link'],
                    "release_date": product['release_date']
                }
            )

    def __identify_card(self, card_name):
        return Card.objects \
            .annotate(similarity=TrigramSimilarity('alias', card_name)) \
            .filter(similarity__gt=0.25) \
            .order_by('-similarity')[0]

