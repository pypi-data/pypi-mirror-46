import os
import sys
import pandas as pd
from datetime import datetime

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import strategy  # noqa: E402


def test_store():
    store = strategy.AlignedStore()
    index = [datetime(2019, 5, 8), datetime(2019, 5, 9), datetime(2019, 5, 10)]
    a = pd.Series(
        [1, 2, 3],
        index
    )
    b = pd.Series(
        [4, 5, 6],
        index
    )
    c = pd.concat([a, b], axis=1)
    c.columns = ['a', 'b']
    store.insert('a', a)
    store.insert('b', b)
    assert c.equals(store.get(['a', 'b']))
    assert c.loc[[datetime(2019, 5, 8)]].equals(
        store.get(['a', 'b'], end=datetime(2019, 5, 8))
    )
    assert store.get_index() == index
