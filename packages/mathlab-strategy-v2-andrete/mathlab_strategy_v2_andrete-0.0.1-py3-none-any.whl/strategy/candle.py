from .ticker import Symbol
from .common import Parameter, Interval
from .expression import Field


class Open():
    pass


class High():
    pass


class Low():
    pass


class Close(Field):
    def __init__(
        self,
        symbol: Symbol = Parameter('symbol'),
        interval: Interval = Parameter('interval'),
    ):
        super().__init__(symbol, 'close', interval)
