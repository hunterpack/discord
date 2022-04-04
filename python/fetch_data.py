import os

import coinmarketcapapi

API_KEY = os.getenv('API_KEY')
cmc = coinmarketcapapi.CoinMarketCapAPI(API_KEY)


def check_map(symbol):
    try:
        data_id_map = cmc.cryptocurrency_map(symbol=symbol)
    except Exception as e:
        print(f'Unable to retrieve data for {symbol}')
    return data_id_map


def fetch_data(ticker):
    data_quote = cmc.cryptocurrency_quotes_latest(symbol=ticker, convert='USD')
    price = data_quote.data[ticker]['quote']['USD']['price']
    return round(price, 2)
