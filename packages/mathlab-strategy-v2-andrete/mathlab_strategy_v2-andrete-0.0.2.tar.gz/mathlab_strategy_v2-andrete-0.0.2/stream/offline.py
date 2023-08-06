from stream.streaming import Streaming
from datetime import datetime
from strategy import Pair, Interval, MarketType, MarketData


class Offline(Streaming):
    def __init__(
            self, pair: Pair, interval: Interval,
            start: datetime, end: datetime, market_type=MarketType.Futures,
            period=20
    ):
        self.period = period
        self.data = MarketData().ohlc_history(pair, interval, start, end, market_type).sort_index(ascending=True)
        self.length = len(self.data)
        self.index = 0

    def start(self, trade):
        while self.index + self.period <= self.length:
            cur_data = self.data[self.index: self.index + self.period]
            self.index += 1
            #instructions = self.run_cycle(cur_data)
            #print(instructions)
