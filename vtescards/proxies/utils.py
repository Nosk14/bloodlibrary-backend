from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
from requests import get


CARD_HEIGHT = 88 * mm
CARD_WIDTH = 63 * mm
MARGIN_LEFT = 10 * mm
MARGIN_BOT = 15 * mm

POSITIONS = [
    (MARGIN_LEFT, MARGIN_BOT + CARD_HEIGHT * 2), (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT + CARD_HEIGHT * 2),
    (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT + CARD_HEIGHT * 2),
    (MARGIN_LEFT, MARGIN_BOT + CARD_HEIGHT), (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT + CARD_HEIGHT),
    (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT + CARD_HEIGHT),
    (MARGIN_LEFT, MARGIN_BOT), (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT), (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT)
]


class ProxyFile:

    def __init__(self, identifier):
        self.id = identifier
        self.canvas = canvas.Canvas(self.id + '.pdf', pagesize=A4)
        self.i = 0

    def add_image(self, url):
        response = get(url)
        image_reader = ImageReader(BytesIO(response.content))
        self.canvas.drawImage(image_reader, POSITIONS[self.i][0], POSITIONS[self.i][1], width=CARD_WIDTH, height=CARD_HEIGHT)
        self.i += 1
        if self.i > 8:
            self.canvas.showPage()
            self.i = 0

    def save(self):
        self.canvas.save()
