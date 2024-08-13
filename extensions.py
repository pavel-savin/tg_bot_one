import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):
        if quote == base:
            raise ConvertionException(f"Введена одинаковая валюта {base}.")

        try:
            quote_ticker, base_ticker = keys[quote], keys[base]
        except KeyError:
            raise ConvertionException(
                f"Неправильно указана переводимые валюты {quote} или {base}."
            )

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать колличество {amount}.")

        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}"
        )
        total_base = json.loads(r.content)[keys[base]]

        total_amount = total_base * amount

        return round(total_amount, 2)
