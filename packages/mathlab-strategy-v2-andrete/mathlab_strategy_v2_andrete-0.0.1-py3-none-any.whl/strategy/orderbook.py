from .common import Value
from .ticker import Symbol
from decimal import Decimal
from typing import Dict, List


class Bid():
    pass


class Ask():
    pass


class Last():
    pass


class OrderBook(Value):
    def __init__(self, symbol: Symbol):
        self.key = '%s_orderbook' % (symbol.get_key())
        super().__init__(self.key)

    def get_best_bid(self):
        pass

    def get_best_ask(self):
        pass

    def get_real_bid(self):
        pass

    def get_real_ask(self):
        pass


class OrderBookEntry():
    def __init__(self, price: Decimal, size: Decimal):
        self.price = price
        self.size = size

    def set_size(self, size: Decimal):
        self.size = size

    def get_size(self) -> Decimal:
        return self.size

    def get_price(self) -> Decimal:
        return self.price


class OrderBookObject():
    def __init__(self):
        self.asks = {}
        self.bids = {}

    def get_asks(self) -> Dict[Decimal, OrderBookEntry]:
        return self.asks

    def get_bids(self) -> Dict[Decimal, OrderBookEntry]:
        return self.bids

    def set_snapshot(
            self, bids: Dict[Decimal, OrderBookEntry],
            asks: Dict[Decimal, OrderBookEntry]
    ):
        self.bids = bids
        self.asks = asks

    def update_bid(self, bid: OrderBookEntry):
        if bid.get_size() > 0:
            self.bids[bid.get_price()] = bid
        elif bid.get_size() == 0:
            if bid.get_price() in self.bids.keys():
                self.bids.pop(bid.get_price())
        else:
            raise NotImplementedError

    def update_ask(self, ask: OrderBookEntry):
        if ask.get_size() > 0:
            self.asks[ask.get_price()] = ask
        elif ask.get_size() == 0:
            if ask.get_price() in self.asks.keys():
                self.asks.pop(ask.get_price())
        else:
            raise NotImplementedError

    def update(
            self, bids: List[OrderBookEntry],
            asks: List[OrderBookEntry]
    ):
        for bid in bids:
            self.update_bid(bid)
        for ask in asks:
            self.update_ask(ask)
