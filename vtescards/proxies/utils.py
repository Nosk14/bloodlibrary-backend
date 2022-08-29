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
LINE_COLOR = (1, 1, 1)

POSITIONS = [
    (MARGIN_LEFT, MARGIN_BOT + CARD_HEIGHT * 2),
    (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT + CARD_HEIGHT * 2),
    (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT + CARD_HEIGHT * 2),
    (MARGIN_LEFT, MARGIN_BOT + CARD_HEIGHT),
    (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT + CARD_HEIGHT),
    (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT + CARD_HEIGHT),
    (MARGIN_LEFT, MARGIN_BOT),
    (MARGIN_LEFT + CARD_WIDTH, MARGIN_BOT),
    (MARGIN_LEFT + CARD_WIDTH * 2, MARGIN_BOT)
]


class ProxyFile:

    def __init__(self):
        self.i = 0
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.canvas.setStrokeColorRGB(*LINE_COLOR)
        self.should_create_page = False

    def __draw_lines(self):
        line_len = 3.5 * mm
        self.canvas.line(POSITIONS[1][0], POSITIONS[1][1] + CARD_HEIGHT + line_len, POSITIONS[7][0], POSITIONS[7][1] - line_len)
        self.canvas.line(POSITIONS[2][0], POSITIONS[2][1] + CARD_HEIGHT + line_len, POSITIONS[8][0], POSITIONS[8][1] - line_len)

        self.canvas.line(POSITIONS[0][0] - line_len, POSITIONS[0][1], POSITIONS[2][0] + CARD_WIDTH + line_len, POSITIONS[2][1])
        self.canvas.line(POSITIONS[3][0] - line_len, POSITIONS[3][1], POSITIONS[5][0] + CARD_WIDTH + line_len, POSITIONS[5][1])

    def add_image(self, url):
        if self.should_create_page:
            self.canvas.showPage()
            self.should_create_page = False
        response = get(url)
        image_reader = ImageReader(BytesIO(response.content))
        self.canvas.drawImage(image_reader, POSITIONS[self.i][0], POSITIONS[self.i][1], width=CARD_WIDTH, height=CARD_HEIGHT)
        self.i += 1
        if self.i > 8:
            self.__draw_lines()
            self.i = 0
            self.should_create_page = True

    def save(self):
        self.__draw_lines()
        self.canvas.save()

    def serve_buffer(self):
        self.buffer.seek(0)
        return self.buffer


if __name__ == '__main__':
    pdf = ProxyFile()
    pdf.save()
