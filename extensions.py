import requests
import json
from config import keys

class ExchangeException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'Невозможно перевести одинаковые валюты: {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не удалось обработать валюту: {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Не удалось обработать валюту: {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'Не удалось обработать представленное количество валюты {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]])

        return total_base