from stream.streaming import Streaming
from datetime import datetime
from strategy import Pair, Interval, MarketType, MarketData
from exchange.okex_public_websocket import OkexPublicWebsocket
from common.okex_common import OkexCommon
import json
import pandas as pd

class Online(Streaming):
    def __init__(
            self, pair: Pair, interval: Interval,
            start: datetime, end: datetime, market_type=MarketType.Futures,
            period=20
    ):
        self.cur_data = MarketData().ohlc_history(pair, interval, start, end, market_type)\
            .sort_index(ascending=True)[-period:][['pair', 'open', 'high', 'low', 'close', 'volume']]
        self.pair = pair
        self.period = period
        self.channels = {
            'future': [],
            'spot': [],
        }
        self.instrument_ids = {
            'future': [],
            'spot': [],
        }
        if market_type == MarketType.Futures:
            self.channels['future'].append('futures/candle{}s'.format(interval.value*60))
            self.instrument_ids['future'].append(OkexCommon().get_latest_future_instrument_id(pair.get_pair()))
        else:
            self.channels['spot'].append('spot/candle{}s'.format(interval.value*60))
            self.instrument_ids['spot'].append(OkexCommon().spot_pair_formatter(pair.get_pair()))

    # TODO: use websocket API to subscribe, enqueue the new one, and dequeue the oldest one.
    def start(self, trade):
        def _handler(ws, msg):
            self.handler(ws, msg)

        OkexPublicWebsocket(self.channels, self.instrument_ids, _handler).run()

    def handler(self, ws, msg):
        data = OkexCommon().inflate(msg)
        if data == 'pong':
            return
        data = json.loads(data)
        if data.get('event') == 'subscribe':
            return
        candle = data['data'][0]['candle']
        candle_formated = {
            'time': candle[0],
            'pair': self.pair.get_pair(),
            'open': float(candle[1]),
            'high': float(candle[2]),
            'low': float(candle[3]),
            'close': float(candle[4]),
            'volume': float(candle[5])
        }
        this_data = pd.DataFrame([candle_formated]).set_index('time')[['pair', 'open','high','low','close','volume']].dropna()
        self.cur_data.loc[this_data.index[0]] = this_data.values[0]
        self.cur_data = self.cur_data[-self.period:].copy()
        print(self.cur_data)

        #instructions = self.run_cycle(self.cur_data)
        #print(instructions)
        # trade by instructions
