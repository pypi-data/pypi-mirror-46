from datetime import datetime

import requests
import pandas
import yaml
import os
from mathlab_pg_api.account_api import AccountApi

from .exchange import Exchanges
from .common import Interval, MarketType
from .ticker import Pair, Symbol
from .singleton import Singleton

#POSTGREST_URL = 'http://localhost:3000/test2'

class AccountData(Singleton):
    def __init__(self):
        self.config = yaml.safe_load(open(os.path.join(os.environ['HOME'], '.mathlab/db_config.yml')))['local']
        self.AccountApi = AccountApi(self.config['host'], self.config['port'], self.config['username'], self.config['password'], self.config['dbname'])
    
    def order_history(
        self, account: Account, pair: Pair, interval: Interval,
        start: datetime, end: datetime
    ) -> pandas.DataFrame:
        # return self.account_api.query('order', 'future', 'okex_chung', 'okex', '')
        return self.account_api.query(exchange_name=pair.get_exchange(), pair=pair.get_pair(), period=interval.value,
                                        start_date=start, end_date=end)