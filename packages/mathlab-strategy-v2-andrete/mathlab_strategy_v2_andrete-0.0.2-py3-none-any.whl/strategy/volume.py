from abc import ABC, abstractmethod
from .account import Account
from .market_data import MarketData
from .currency import Currency


class Volume(ABC):
    @abstractmethod
    def get_volume(self, account: Account, market: MarketData):
        pass


class FixedVolume(Volume):
    def __init__(self, quantity: int, unit: Currency):
        self.quantity = quantity
        self.unit = unit

    def get_volume(self, account: Account, market: MarketData):
        return 0


class PercentVolume(Volume):
    def __init__(self, percent: float):
        self.percent = percent
