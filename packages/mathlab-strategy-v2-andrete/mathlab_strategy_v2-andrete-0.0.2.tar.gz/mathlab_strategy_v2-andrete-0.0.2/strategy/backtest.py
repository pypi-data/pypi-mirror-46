from datetime import datetime
from decimal import Decimal
from typing import List

import pandas
import numpy

from .framework import Strategy
from .market_data import MarketData
from .ticker import Pair
from .common import Interval, Instructions, MarketType
from .trade import Side
from .currency import Currency
from .store import AlignedStore


class BacktestResult():
    pass


class BacktestConfig():
    def __init__(
        self, pairs: List[Pair], interval: Interval,
        start: datetime, end: datetime, skip: int = 0,
        maker_fee: Decimal = Decimal('0.002'),
        taker_fee: Decimal = Decimal('0.002')
    ):
        self.pairs = pairs
        self.interval = interval
        self.start = start
        self.end = end
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.skip = skip


class Backtest():
    def __init__(self, config: BacktestConfig):
        self.config = config

    def set_config(self, config: BacktestConfig) -> None:
        self.config = config

    def get_config(self) -> BacktestConfig:
        return self.config

    def data_prepare(self) -> dict:
        ohlcs = {}
        for pair in self.config.pairs:
            ohlcs[pair] = MarketData().ohlc_history(
                pair, self.config.interval,
                self.config.start, self.config.end,
                MarketType.Spot
            ).sort_index(ascending=True)
        return pandas.concat(ohlcs, axis=1)

    def Drawdown(input_data):
        df = pandas.DataFrame(input_data, columns=['y'], dtype='float')
        df['maxY'] = df['y'].rolling(10**8, min_periods=1).max()
        df['drop'] = df['maxY'] - df['y']
        df['maxdrop'] = df['drop'].rolling(10**8, min_periods=1).max()
        maxdrop = df['maxdrop'].max()
        return maxdrop

    def run(self, strategy: Strategy):
        bt_status_list = []
        bt_status = {
                        Currency('ETH').name: Decimal("10000"),
                        Currency('ETH').name + '_equity': Decimal("0."),
                        'equity': Decimal("0."),
                        'buy_volume': Decimal("0."),
                        'sell_volume': Decimal("0."),
                        'buy_trade_cnt': 0,
                        'sell_trade_cnt': 0,
                    }
        for pair in self.config.pairs:
            bt_status[pair.quote_currency.name] = Decimal("0")
            bt_status[pair.quote_currency.name + '_equity'] = Decimal("0.")
            bt_status[pair.quote_currency.name + '_trade'] = 0
            bt_status[pair.quote_currency.name + '_close'] = 0

        ohlcs = self.data_prepare()
        prices = {}
        candles_count = 0
        for index, row in ohlcs.iterrows():
            new_row = {}
            for item in row.iteritems():
                if not pandas.isna(item[1]):
                    new_row['%s.%s.%s' % (
                        item[0][0], item[0][1], self.config.interval
                    )] = item[1]
                    if item[0][1] == 'close':
                        prices[item[0][0]] = item[1]
            AlignedStore().update_row(new_row, index)
            candles_count += 1
            if candles_count < self.config.skip:
                continue

            try:
                strategy.on_tick()
            except Exception as e:
                print('strategy error {}'.format(e))

            for instruction in Instructions().get_all():
                print(index, instruction, prices[instruction.get_symbol()])
                pair = str(instruction.get_symbol()).split('@')[0]
                side = instruction.get_side()
                # print(index, close.get_key(), ma)
                quote_name, base_name = pair.split('/')
                price = prices[instruction.get_symbol()]
                volume = instruction.volume
                # print(index, close, type(volume))

                if side == Side.BUY:
                    bt_status[quote_name] += volume
                    bt_status[base_name] -= volume * price * \
                        (1 + self.config.taker_fee)
                    # bt_status[quote_name] += volume
                    # bt_status[base_name] -= volume * close
                    bt_status['buy_volume'] += volume
                    bt_status['buy_trade_cnt'] += 1
                elif side == Side.SELL:
                    bt_status[quote_name] -= volume * \
                        (1 + self.config.taker_fee)
                    bt_status[base_name] += volume * price
                    # bt_status[quote_name] -= volume
                    # bt_status[base_name] += volume * close
                    bt_status['sell_volume'] += volume
                    bt_status['sell_trade_cnt'] += 1
            bt_status['equity'] = Decimal("0")
            bt_status['ETH_equity'] = bt_status['ETH']
            for pair in self.config.pairs:
                quote = pair.quote_currency.name
                price = prices[pair]
                bt_status[quote + '_equity'] = price * bt_status[quote]

            for key in bt_status:
                if '_equity' in key:
                    bt_status['equity'] += bt_status[key]
            bt_status_list.append([index, bt_status.copy()])
            Instructions().clear()
        x, y = [], []
        for time, dic in bt_status_list:
            # x.append(dp.parse(time))
            x.append(time)
            # x.append(dp.parse(time).strftime('%d %H:%M'))
            y.append(dic['equity'])
        print(len(bt_status_list), len(x), len(y))
        if len(bt_status_list) == 0:
            print('no data')
            return
        bt_status_final = bt_status_list[-1][1]
        message = 'final result\n'
        message += '''equity:{}
buy_volume:{}
sell_volume:{}
buy_trade_cnt:{}
sell_trade_cnt:{}'''
        print(
            message.format(
                    bt_status_final['equity'],
                    bt_status_final['buy_volume'],
                    bt_status_final['sell_volume'],
                    bt_status_final['buy_trade_cnt'],
                    bt_status_final['sell_trade_cnt']
                    )
        )
        print('drawdown', Backtest.Drawdown(y))
        import matplotlib.pyplot as plt
        plt.xlabel('datetime')
        plt.ylabel('net asset:ETH')
        plt.title('backtest')
        plt.gcf().autofmt_xdate()
        plt.xticks(rotation=90)
        plt.plot_date(x, y, color='b', linestyle='-', marker=',', label='okex')
        plt.legend(loc='best')
        plt.show()
