import json
import pickle
import pprint
from datetime import datetime
from utils3 import assertTypes


class MobyStock:
    def __init__(self, json_dict, do_nothing=False, edit_id=None):
        if not do_nothing:
            self.ticker: str = self._get_ticker_from_content(json_dict['content'])
            self.title: str = json_dict['title']
            self.dt: datetime = self._generate_dt_from_str(json_dict['date'])
            self.subsections = json_dict['subsections']

            target, upside, original = self._extract_price_and_upside(json_dict['summary'])
            self.target_price: float = target
            self.upside: float = upside
            self.original_price: float = original

            self.historical_data: list = []
            self.misc: dict = json_dict
            self._edit_id = edit_id

    @property
    def edit_id(self):
        try:
            return self._edit_id
        except AttributeError:
            return None

    @staticmethod
    def _generate_dt_from_str(date_str: str) -> datetime:
        # sample 2024-11-22T21:52:00+01:00

        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')

    @staticmethod
    def _extract_price_and_upside(summary):
        target_price = float(summary.lower().split('$')[1].split(' ')[0].split('\xa0')[0].replace(',', ''))
        upside = float(summary.lower().split('(')[1].split('%')[0])
        original_price = target_price / (1 + upside / 100)
        return target_price, upside, original_price

    @staticmethod
    def _get_ticker_from_content(content_str):
        ticker = content_str.split('charting/?ticker=')[1].split('"')[0]
        return ticker

    @classmethod
    @assertTypes((str, str, datetime, list, float, float, float, list, dict), class_method=True, auto_convert=False)
    def from_values(cls, ticker, title, dt, subsections, target_price, upside, original_price, historical_data, misc,
                    **kwargs):
        ms = cls({}, do_nothing=True)
        ms.ticker = ticker
        ms.title = title
        ms.dt = dt
        ms.subsections = subsections
        ms.target_price = target_price
        ms.upside = upside
        ms.original_price = original_price
        ms.historical_data = historical_data
        ms.misc = misc
        return ms

    def pnl_in_time_percentage(self, t_minus_today):
        data = self.historical_data[0]['Close/Last']
        return (float(data[t_minus_today].replace('$', '')) - self.original_price) / self.original_price


def get_pages(pg=3):
    import requests
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'JWT': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDQ2NzM5LCJleHAiOjE3Mzg1NDA5OTgsImVtYWlsIjoic2FsbWFuZmFyaXMyMDA1QGhvdG1haWwuY29tIiwiY3VzdG9tIjpudWxsLCJ0eXBlIjoiYWNjZXNzIn0.FGmKGygfTOV8gBG5x8uOQa34WMGH70rnNMC1bEic-5c',
        'JWT-User-Id': '446739',
        'Origin': 'https://app.moby.co',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    params = {
        'category_id': '0',
        'page': '2',
        'per_page': '24'
    }

    response = requests.get('https://api.ww-api.com/front/restricted/get_items/3277999/55915304/', params=params,
                            headers=headers)
    with open('sample_pg={}.json'.format(pg), 'w') as f:
        f.write(response.text)


def sample_to_moby_stock(sample):
    js = json.loads(open(sample).read())['items']
    moby_stocks = []
    for j in js:
        msx = MobyStock(j)
        moby_stocks.append(msx)
        d = msx.__dict__
        d['misc'] = {}
        pprint.pprint(d)
        _ = MobyStock.from_values(**d)
    return moby_stocks


if __name__ == '__main__':

    files = [
        'sample.json',
        'sample_pg=3.json',
        'sample_pg=4.json',
        'sample_pg=5.json'
    ]

    stks = []
    for file in files:
        stks.extend(sample_to_moby_stock(file))

    with open('moby_stocks.pkl', 'wb') as f:
        pickle.dump(stks, f)

    print('Total stocks:', len(stks))

    # for i in range(3, 6, 1):
    #     get_pages(i)
    #     input('press enter to continue')
