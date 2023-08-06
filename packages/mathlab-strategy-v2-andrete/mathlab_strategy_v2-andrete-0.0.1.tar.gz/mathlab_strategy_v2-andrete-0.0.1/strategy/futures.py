from datetime import datetime

from .exchange import Exchange
from .index import Index
from .ticker import Symbol


class IndexFutures(Symbol):
    def __init__(
        self, index: Index, expire_date: datetime, exchange: Exchange
    ):
        self.index = index
        self.expire_date = expire_date
        self.exchange = exchange
