import os
from requests import get
import logging


class VTESDecksClient:
    BASE_URL = 'https://api.vtesdecks.com/1.0/'

    def __init__(self):
        pass

    def get_tournament_decks(self, offset, limit, years=None):
        params = {'offset': offset, 'limit': limit, 'type': 'TOURNAMENT'}
        if years:
            params['year'] = years
        rs = get(self.BASE_URL + 'decks', params=params)

        return rs.json()

    def get_deck_info(self, deck_id):
        rs = get(self.BASE_URL + 'decks/' + deck_id)

        return rs.json()


class VEKNClient:
    BASE_URL = 'https://www.vekn.net/api/vekn/'

    def __init__(self):
        self.auth_header = {'Authorization': 'Bearer ' + os.getenv("VEKN_API_TOKEN")}

    def get_event(self, event_id):
        rs = get(self.BASE_URL + '/event/' + event_id, headers=self.auth_header)

        try:
            data = rs.json()['data']['events']
            return data[0] if data else None

        except Exception:
            logging.error(event_id)
            logging.error(rs.json())
