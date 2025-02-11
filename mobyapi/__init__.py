import requests
import warnings
from utils3.networking import Session
from mobyapi.randos import *
from dataclasses import asdict

_endpoints = {
    'top-picks': 'https://api.ww-api.com/front/get_items/3277999/55915304/?category_index=0'
}



def update_endpoints(new_endpoints):
    msg = 'Use this function sparingly, it is not recommended to update the endpoints unless you know what you are doing.'
    warnings.warn(msg)
    _endpoints.update(new_endpoints)

class MobyException(Exception):
    pass

class NoMoreDataAvailable(MobyException):
    pass

class TopPicksIterator:
    def __init__(self, base_url, session, decode_json=True):
        self._base_url = base_url
        self._session = session
        self._next_page = None
        self._decode_json = decode_json

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_page is None:
            self._next_page = self._base_url
        else:
            self._next_page = self._next_page

        if len(self._next_page) == 0:
            raise NoMoreDataAvailable('API returned invalid next page')

        response = self._session.get(self._next_page)
        data = ApiResponse(**response.json())
        if len(data.items) == 0:
            raise NoMoreDataAvailable('API returned empty items')

        self._next_page = data.next_page

        if self._decode_json:
            return data

        return response.json()


class MobyAPI:
    def __init__(self):
        self._headers = generate_headers()
        self._session = Session(headers=self._headers)


    def top_picks(self, **kwargs):
        return TopPicksIterator(_endpoints['top-picks'], self._session, **kwargs)

class MobyAuthenticatedAPI(MobyAPI):
    def __init__(self, jwt, jwt_user_id):
        super().__init__()
        self._headers['JWT'] = jwt
        self._headers['JWT-User-Id'] = jwt_user_id
        self._session = Session(headers=self._headers)
        update_endpoints({
            'top-picks': _endpoints['top-picks'].replace('get_items', 'restricted/get_items')
        })


