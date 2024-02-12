import datetime
import logging
from html.parser import HTMLParser

import requests
from django.contrib.postgres.search import TrigramSimilarity
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from api.models import Card
from pod.models import CardShop


class DTCCollector:
    WEB_URL = "https://www.drivethrucards.com/browse/pub/12056/Black-Chantry-Productions/subcategory/30619_34256/VTES-Legacy-Card-Singles?sort=4a&pfrom=0.10&pto=0.59&page={0}"

    def __init__(self):
        self.__session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.__session.mount('http://', adapter)
        self.__session.mount('https://', adapter)

    def collect_cards(self):
        raw_cards = self.__get_cards_from_web()
        self.__parse_raw_cards(raw_cards)

    def __get_cards_from_web(self):
        raw_cards = []
        for page in range(1, 25):
            html = self.__get_html(DTCCollector.WEB_URL.format(page))
            parser = DriveThruParser()
            parser.feed(html)
            raw_cards.extend(parser.cards)
        return raw_cards

    def __get_html(self, url):
        rs = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        return rs.text

    def __identify_card(self, card_name):
        return Card.objects \
            .annotate(similarity=TrigramSimilarity('alias', card_name)) \
            .filter(similarity__gt=0.25) \
            .order_by('-similarity')[0]

    def __parse_raw_card(self, raw_card):
        if "Hell-for-Leather" in raw_card['name']:
            name = "Hell-for-Leather"
        elif "Ashur" in raw_card['name']:
            name = "Ashur Tablet"
        else:
            name = raw_card['name'].split("-", 1)[1].strip()
            if "-" in name:
                name = name.rsplit("-", 1)[0].strip()
        link = raw_card['link'].rsplit('?')[0].rsplit('/', 1)[0]
        card = self.__identify_card(name)
        release_date = raw_card['release_date']

        CardShop.objects.update_or_create(
            card=card,
            shop="DTC",
            defaults={
                "link": link,
                "release_date": datetime.datetime.strptime(release_date, "%Y-%m-%d").date()
            }
        )

    def __parse_raw_cards(self, raw_cards):
        for raw_card in raw_cards:
            self.__parse_raw_card(raw_card)


class DriveThruParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.cards = []
        self.__is_parsing_card = False
        self.__card_link = None
        self.__card_name = None
        self.__release_date = None

    def error(self, message):
        logging.error(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr' and ('class', 'dtrpgListing-row') in attrs:
            self.__is_parsing_card = True
        elif self.__is_parsing_card and tag == 'td' and ('class', 'main') in attrs:
            pass
        elif self.__is_parsing_card:
            if tag == 'a' and self.__card_link is None:
                self.__card_link = list(filter(lambda att: att[0] == 'href', attrs))[0][1]
            elif tag == 'img' and self.__card_name is None:
                self.__card_name = list(filter(lambda att: att[0] == 'alt', attrs))[0][1]

    def handle_endtag(self, tag):
        if tag == 'tr' and self.__is_parsing_card:
            self.__is_parsing_card = False
            self.cards.append({'name': self.__card_name, 'link': self.__card_link, 'release_date': self.__release_date})
            self.__card_name = None
            self.__card_link = None
            self.__release_date = None

    def handle_data(self, data):
        if self.__is_parsing_card and data.startswith("Date Added:"):
            self.__release_date = data.split(':')[1].strip()
