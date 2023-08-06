from datetime import datetime
from typing import List

import pandas as pd
import numpy as np

from .singleton import Singleton


class AlignedStore(Singleton):
    def __init__(self):
        self.df = pd.DataFrame()

    def update_column(self, key: str, series: pd.Series):
        self.df[key] = series

    def update_row(self, new_row: dict, index: datetime):
        for key in new_row.keys():
            if key not in self.df.columns:
                self.df.insert(0, key, np.nan)
        # self.df.append()
        self.df.loc[index] = pd.Series(new_row)

    def get(
            self, keys: List[str] = None,
            start: datetime = None, end: datetime = None
    ) -> pd.DataFrame:
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
