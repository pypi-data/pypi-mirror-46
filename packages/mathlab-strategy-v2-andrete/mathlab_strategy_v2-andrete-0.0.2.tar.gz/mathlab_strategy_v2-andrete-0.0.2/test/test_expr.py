import os
import sys
import math

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import strategy  # noqa: E402


def test_expr():
    a = strategy.Const(2)
    b = strategy.Const(1)
    assert (a + b).get_value() == 3
    assert (a - b).get_value() == 1
    assert (a * b).get_value() == 2
    assert (a / b).get_value() == 2
    close = strategy.Field(
        strategy.Pair(
                strategy.Currencies.EOS,
                strategy.Currencies.ETH,
                strategy.Exchanges.OKEX
        ), 'close', strategy.Interval.M1
    )
    test_data = [1, 2, 3, 4, 5]
    n = 5
    mean = sum(test_data) / n
    sd = math.sqrt(sum([(x - mean)**2 for x in test_data]) / n) 
    close.push(test_data)
    sma = strategy.SMA(close, n)
    assert sma.get_value() == mean
    std = strategy.STDDEV(close, n)
    assert std.get_value() == sd
