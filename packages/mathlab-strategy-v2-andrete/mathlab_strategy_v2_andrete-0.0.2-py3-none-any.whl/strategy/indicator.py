import talib
import numpy as np
import pandas as pd
from collections import deque
from decimal import Decimal
import math

class Indicator():

    @staticmethod
    def SMA(input_data, timeperiod=100):
        result = []
        q = deque(maxlen=timeperiod)
        for price in input_data:
            q.append(price)
            if len(q) < timeperiod:
                result.append(np.NAN)
            else:
                sma = sum([item for item in q]) / Decimal(timeperiod)
                result.append(sma)
        return pd.Series(result, index=input_data.index)

    @staticmethod
    def STD(input_data, length=100):
        result = []
        q = deque(maxlen=length)
        for price in input_data:
            q.append(price)
            if len(q) < length:
                result.append(np.NAN)
            else:
                mean = sum([item for item in q]) / Decimal(length)
                var = sum([Decimal(math.pow(item - mean, 2)) for item in q]) 
                var = var / Decimal(length)
                std = math.sqrt(var)
                result.append(var)
        return pd.Series(result, index=input_data.index)
    
    @staticmethod
    def Drawdown(input_data):
        df = pd.DataFrame(input_data, columns=['y'], dtype='float')
        df['maxY'] = df['y'].rolling(10**8,min_periods=1).max()
        df['drop'] = df['maxY'] - df['y']
        df['maxdrop'] = df['drop'].rolling(10**8,min_periods=1).max()
        maxdrop = df['maxdrop'].max() 
        return maxdrop

    @staticmethod
    def Sharpe(input_data):
        pass

'''
close = np.random.random(100)
output = talib.SMA(close, 10)
print(output, type(output))
result = SMA(close, 10)
print(result)
'''

