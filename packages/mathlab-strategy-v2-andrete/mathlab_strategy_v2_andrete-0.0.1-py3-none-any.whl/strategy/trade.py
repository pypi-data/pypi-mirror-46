from decimal import Decimal
from enum import Enum

from .ticker import Symbol
from .volume import Volume
from .common import Instructions, Instruction


class Side(Enum):
    BUY = 'buy'
    SELL = 'sell'


class placeOrder(Instruction):
    def __init__(self, symbol: Symbol, side: Side, volume, price=None):
        Instructions().add(self)
        self.symbol = symbol
        self.side = side
        self.volume = volume
        self.price = price

    def get_symbol(self):
        return self.symbol

    def get_side(self):
        return self.side

    def get_volume(self):
        return self.volume

    def __str__(self):
        return 'order %s %s %s %s' % (
            self.symbol, self.side, self.volume, self.price
        )


class placeLimitOrder(placeOrder):
    def __init__(
        self, symbol: Symbol, side: Side, volume: Volume, price: Decimal
    ):
        super().__init__(symbol, side, volume, price)


class placeMarketOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        super().__init__()
        self.symbol = symbol
        self.side = side
        self.volume = volume


class placeMakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        super().__init__(symbol, side, volume)


class placeTakerOrder(placeOrder):
    def __init__(self, symbol: Symbol, side: Side, volume: Volume):
        super().__init__(symbol, side, volume)
