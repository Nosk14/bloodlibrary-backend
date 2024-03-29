from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
from requests import get
from requests.auth import HTTPBasicAuth
import os
import jwt


CARD_HEIGHT = 88 * mm
CARD_WIDTH = 63 * mm
MARGIN_LEFT = 10 * mm
MARGIN_BOT = 15 * mm
DEFAULT_LINE_COLOR = (1, 1, 1)

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

    def __init__(self, line_color=DEFAULT_LINE_COLOR):
        self.i = 0
        self.line_color = line_color
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.canvas.setStrokeColor(self.line_color)
        self.should_create_page = False

    def __draw_lines(self):
        line_len = 3.5 * mm
        self.canvas.line(POSITIONS[1][0], POSITIONS[1][1] + CARD_HEIGHT + line_len, POSITIONS[7][0], POSITIONS[7][1] - line_len)
        self.canvas.line(POSITIONS[2][0], POSITIONS[2][1] + CARD_HEIGHT + line_len, POSITIONS[8][0], POSITIONS[8][1] - line_len)

        self.canvas.line(POSITIONS[0][0] - line_len, POSITIONS[0][1], POSITIONS[2][0] + CARD_WIDTH + line_len, POSITIONS[2][1])
        self.canvas.line(POSITIONS[3][0] - line_len, POSITIONS[3][1], POSITIONS[5][0] + CARD_WIDTH + line_len, POSITIONS[5][1])

    def add_image(self, url, needs_authorization=False):
        if self.should_create_page:
            self.canvas.showPage()
            self.canvas.setStrokeColor(self.line_color)
            self.should_create_page = False
        if needs_authorization:
            auth = HTTPBasicAuth(os.getenv('STATICS_USER'), os.getenv('STATICS_PASSWORD'))
            response = get(url, auth=auth)
        else:
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


def is_tester(token):
    if not token:
        return False
    return __is_valid_token(token) and __has_tester_permission(token)


def __is_valid_token(token):
    rs = get('http://api.vtesdecks.com/1.0/user/validate', headers={'Authorization': token})
    return rs.status_code == 200 and rs.text == 'true'


def __has_tester_permission(token):
    result = jwt.decode(token, options={"verify_signature": False})
    return 'tester' in result and result['tester']


if __name__ == '__main__':
    pdf = ProxyFile()
    pdf.save()
