import json
import redis
import requests
from config import keys
from datetime import datetime


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: float):
        red = MyRedis()
        data = red.get_rate(quote, base)
        if data is not None and Converter.actual(data[1]):
            rate = data[0]
        else:
            rate = Converter.update_rates(quote, base)
        new_amount = round(float(amount) * float(rate), 2)
        return new_amount

    @staticmethod
    def get_rates(quote, base):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        rate = json.loads(r.content)[base]
        return rate

    @staticmethod
    def actual(date):
        diff = datetime.now() - datetime.fromisoformat(date)
        return True if diff.total_seconds() < 3600 else False

    @staticmethod
    def update_rates(quote, base):
        print(f'Актуализирую данные по {quote}:{base}')
        rate = Converter.get_rates(quote, base)
        red = MyRedis()
        red.add_rate(quote, base, rate)
        return rate


class MyRedis:
    def __init__(self):
        self.red = redis.Redis(host='127.0.0.1')

    def add_rate(self, quote, base, rate):
        self.red.set(f'{quote}:{base}', json.dumps((rate, datetime.now().isoformat())))

    def get_rate(self, quote, base):
        data = self.red.get(f'{quote}:{base}')
        return None if data is None else json.loads(data)


