import random
from datetime import datetime
from utils3 import assertTypes
from dataclasses import dataclass, field
from typing import List, Dict, Optional


def generate_headers():
    # Random platform selection and mobile detection
    platforms = ["macOS", "Windows", "Linux", "Android", "iOS"]
    platform = random.choice(platforms)
    is_mobile = "?1" if platform in ["Android", "iOS"] else "?0"

    # Platform-specific OS string variations
    os_variants = {
        "macOS": [
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_6_5",
            "Macintosh; Apple M1 Mac OS X 12_6_1",
            "Macintosh; Intel Mac OS X 13_4_0"
        ],
        "Windows": [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.3; Win64; x64",
            "Windows NT 6.1; WOW64"
        ],
        "Linux": [
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
            "X11; Fedora; Linux x86_64"
        ],
        "Android": [
            "Linux; Android 10; SM-G981B",
            "Linux; Android 11; Pixel 5",
            "Linux; Android 12; SM-S901B"
        ],
        "iOS": [
            "iPhone; CPU iPhone OS 14_7 like Mac OS X",
            "iPad; CPU OS 15_4 like Mac OS X",
            "iPhone; CPU iPhone OS 16_2 like Mac OS X"
        ]
    }

    # Browser version generation
    chrome_major = random.randint(100, 140)
    chrome_version = f"{chrome_major}.0.0.0"

    # Construct headers
    return {
        "sec-ch-ua-platform": f'"{platform}"',
        "Referer": f"https://app.moby.co/?rnd={random.randint(1000, 9999)}",
        "User-Agent": (
            f"Mozilla/5.0 ({random.choice(os_variants[platform])}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome_version} Safari/537.36"
        ),
        "sec-ch-ua": (
            f'"Not A(Brand";v="8", "Chromium";v="{chrome_major}", '
            f'"Google Chrome";v="{chrome_major}"'
        ),
        "sec-ch-ua-mobile": is_mobile,
        "Accept": "application/json, text/plain, */*"
    }


@dataclass
class Image:
    id: str
    url: str
    otherImagesUrl: Dict[str, str]


@dataclass
class Meta:
    title: str
    description: str


@dataclass
class Item:
    type: str
    subtype: str
    id: int
    author: str
    title: str
    date: str
    summary: str
    content: str
    images: List[Image]
    isFeatured: str
    smallThumbnail: str
    thumbnail: str
    originalThumbnail: str
    largeThumbnail: str
    xLargeThumbnail: str
    xxLargeThumbnail: str
    isHeadline: int
    authorAvatarUrl: str
    slug: str
    meta: Meta
    purchaseUrl: str
    purchaseUrlAndroid: str
    length: int
    nbcomments: int
    url: str
    subsections: Dict[str, List[str]]
    isFullVersion: bool
    availableForSubscriptions: List[str]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ApiResponse:
    def __init__(self, items: List[dict], next_page: str, stat: str, dedup: bool, http_status_code: int,
                 generated_in: float, cached_at: int):
        self.items = [Item(**item) for item in items]
        self.next_page = next_page
        self.stat = stat
        self.dedup = dedup
        self.http_status_code = http_status_code
        self.generated_in = generated_in
        self.cached_at = cached_at






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


