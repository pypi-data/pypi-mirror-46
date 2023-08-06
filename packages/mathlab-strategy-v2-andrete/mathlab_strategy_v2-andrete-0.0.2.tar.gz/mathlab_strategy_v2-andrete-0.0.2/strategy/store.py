from datetime import datetime
from typing import List
from decimal import Decimal

import pandas

from .singleton import Singleton


class AlignedStore(Singleton):
    def __init__(self):
        self.df = pandas.DataFrame()

    def update_column(self, key: str, series: pandas.Series):
        series = series.astype(object)
        # series[series.isna()] = Decimal('NaN')
        self.df[key] = series

    def update_row(self, new_row: dict, index: datetime):
        for key in new_row.keys():
            if key not in self.df.columns:
                self.df.insert(0, key, Decimal('NaN'))
        self.df.loc[index] = pandas.Series(new_row)
        ffill_index = self.df.index.get_loc(index) - 1
        for key, value in self.df.loc[index].items():
            if pandas.isna(value):
                self.df[key][index] = self.df.iloc[ffill_index][key]

    def get(
            self, keys: List[str] = None,
            start: datetime = None, end: datetime = None
    ) -> pandas.DataFrame:
        if self.df.shape[0] == 0:
            return self.df
        if start is None:
            start = self.df.index[0]
        if end is None:
            end = self.df.index[-1]
        if keys is None:
            keys = self.df.columns.tolist()
        return self.df.loc[
            (self.df.index >= start) & (self.df.index <= end),
            keys
        ]

    def get_index(self):
        return self.df.index.tolist()
