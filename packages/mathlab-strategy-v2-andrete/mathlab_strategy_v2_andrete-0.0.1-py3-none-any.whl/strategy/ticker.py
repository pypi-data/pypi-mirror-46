from .currency import Currency
from .exchange import Exchange

from abc import ABC, abstractmethod


class Symbol(ABC):
    @abstractmethod
    def get_exchange(self):
        return NotImplemented

    @abstractmethod
    def get_key(self):
        return NotImplemented

    def __hash__(self):
        return hash(self.get_key())

    def __eq__(self, obj):
        return self.get_key() == obj.get_key()


class Spot(Symbol):
    def __init__(self, currency: Currency, exchange: Exchange):
        self.currency = currency
        self.exchange = exchange

    def get_exchange(self):
        return self.exchange

    def get_currency(self):
        return self.currency


class Pair(Symbol):
    def __init__(self, quote: Currency, base: Currency, exchange: Exchange):
        self.quote_currency = quote
        self.base_currency = base
        self.exchange = exchange

    def get_exchange(self):
        return self.exchange

    def get_key(self):
        return str(self)

    def get_pair(self):
        return '%s/%s' % (
            self.quote_currency,
            self.base_currency
        )

    def __str__(self):
        return '%s/%s@%s' % (
            self.quote_currency,
            self.base_currency,
            self.exchange
        )

    def __lt__(self, right):
        if isinstance(right, Pair):
            return str(self) < str(right)
        return NotImplemented
