import os

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


def fetch_price(**kwargs):
    url = f"{BASE_URL}/quotes/latest"
    parameters = {
        "convert": "USD",
    }

    params = {**parameters, **kwargs}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        if "symbol" in params:
            ticker = "symbol"
        elif "id" in params:
            ticker = "id"

        price = round(data["data"][params[ticker]]["quote"]["USD"]["price"], 4)
        return price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def check_map(symbol):
    url = f"{BASE_URL}/map"

    params = {'symbol': symbol}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        symbol_map = data['data']
        return symbol_map

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
