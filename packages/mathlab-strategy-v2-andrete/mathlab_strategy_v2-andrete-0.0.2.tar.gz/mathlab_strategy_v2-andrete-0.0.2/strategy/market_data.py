from datetime import datetime

import requests
import pandas
import yaml
import os
from mathlab_pg_api.futures_api import FuturesApi
from mathlab_pg_api.spot_api import SpotApi

from .exchange import Exchanges
from .common import Interval, MarketType
from .ticker import Pair, Symbol
from .singleton import Singleton

#POSTGREST_URL = 'http://localhost:3000/test2'


class MarketData(Singleton):
    def __init__(self):
        self.config = yaml.safe_load(open(os.path.join(os.environ['HOME'], '.mathlab/db_config.yml')))['local']
        self.futures_api = FuturesApi(self.config['host'], self.config['port'], self.config['username'], self.config['password'], self.config['dbname'])
        self.spot_api = SpotApi(self.config['host'], self.config['port'], self.config['username'], self.config['password'], self.config['dbname'])

    # Old version
    #def ohlc_history(
    #    self, pair: Pair, interval: Interval,
    #    start: datetime, end: datetime
    #) -> pandas.DataFrame:
    #    if pair.get_exchange() != Exchanges.Binance:
    #        return NotImplemented
    #    if not isinstance(pair, Pair):
    #        return NotImplemented
    #    if interval != Interval.M1:
    #        return NotImplemented
    #    params = {
    #        'and': '(time.gte.%s,time.lte.%s)' % (
    #            start.isoformat(), end.isoformat()),
    #        'pair': 'eq.%s%s' % (pair.quote_currency, pair.base_currency),
    #        'exchange_id': 'eq.6',
    #        'period': 'eq.1',
    #        'order': 'time'
    #    }
    #    r = requests.get(POSTGREST_URL, params=params)
    #    if r.status_code == 200:
    #        df = pandas.DataFrame(r.json())
    #        df.set_index('time', inplace=True)
    #        return df
    #    return NotImplemented

    def ohlc_history(
        self, pair: Pair, interval: Interval,
        start: datetime, end: datetime, market_type = MarketType.Futures
    ) -> pandas.DataFrame:
        if market_type == MarketType.Futures:
            api = self.futures_api
        else:
            api = self.spot_api
        return api.candles(exchange_name=pair.get_exchange(), pair=pair.get_pair(), period=interval.value,
                                        start_date=start, end_date=end)
