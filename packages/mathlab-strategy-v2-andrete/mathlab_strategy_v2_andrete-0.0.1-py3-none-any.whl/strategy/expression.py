from abc import abstractmethod
from .ticker import Symbol
from .config import Config
from .store import AlignedStore
from .common import Interval
import talib
import pandas as pd


class Expr():
    def __init__(self, interval: Interval):
        self.interval = interval
        self.data = []

    def get_interval(self):
        return self.interval

    @abstractmethod
    def get_key(self):
        raise NotImplementedError()

    def __add__(self, right):
        if isinstance(right, Expr):
            return Add(
                self, right,
                min(self.get_interval(), right.get_interval())
            )
        else:
            return Add(self, right, self.get_interval())

    def __sub__(self, right):
        if isinstance(right, Expr):
            return Substract(
                self, right,
                min(self.get_interval(), right.get_interval())
            )
        else:
            return Substract(self, Const(right), self.get_interval())

    def __mul__(self, right):
        if isinstance(right, Expr):
            return Multiple(
                self, right,
                min(self.get_interval(), right.get_interval())
            )
        else:
            return Multiple(self, Const(right), self.get_interval())

    def __truediv__(self, right):
        if isinstance(right, Expr):
            return Divide(
                self, right,
                min(self.get_interval(), right.get_interval())
            )
        else:
            return Divide(self, Const(right), self.get_interval())

    def __gt__(self, right):
        return self.get_value() > right.get_value()

    def __str__(self):
        return str(self.get_value())

    def push(self, data2push):
        if isinstance(data2push, list):
            self.data.extend(data2push)
        else:
            self.data.append(data2push)

    def get_list(self):
        return self.data

    def get_ref(self, ref: int):
        return self.get_list()[-ref]

    def get_recent(self, count: int):
        return self.get_list()[-count:]

    def get_value(self):
        return self.get_list()[-1]

    def __bool__(self):
        return self.get_value() is True


class Operator(Expr):
    def get_value(self):
        if Config().isLazyEval():
            return AlignedStore().get(self.get_key())
        else:
            return self.calculate()

    @abstractmethod
    def calculate(self):
        raise NotImplementedError()


class BinaryOperator(Expr):
    def get_value(self):
        if Config().isLazyEval():
            return AlignedStore().get(self.get_key())
        else:
            return self.calculate()


class Add(BinaryOperator):
    def __init__(self, left: Expr, right: Expr, interval: Interval):
        super().__init__(interval)
        self.left = left
        self.right = right

    def calculate(self):
        return self.left.get_value() + self.right.get_value()


class Substract(BinaryOperator):
    def __init__(self, left: Expr, right: Expr, interval: Interval):
        super().__init__(interval)
        self.left = left
        self.right = right

    def calculate(self):
        return self.left.get_value() - self.right.get_value()


class Multiple(BinaryOperator):
    def __init__(self, left: Expr, right: Expr, interval: Interval):
        super().__init__(interval)
        self.left = left
        self.right = right

    def calculate(self):
        return self.left.get_value() * self.right.get_value()


class Divide(BinaryOperator):
    def __init__(self, left: Expr, right: Expr, interval: Interval):
        super().__init__(interval)
        self.left = left
        self.right = right

    def calculate(self):
        return self.left.get_value() / self.right.get_value()


class Const(Expr):
    def __init__(self, value):
        super().__init__(Interval.Constant)
        super().push(value)

    def get_key(self):
        return 'Const(%s)' % (str(self.value))


class Field(Expr):
    def __init__(self, symbol: Symbol, field_name: str, interval: Interval):
        super().__init__(interval)
        self.symbol = symbol
        self.name = field_name

    def get_key(self):
        return '%s.%s.%s' % (self.symbol, self.name, self.get_interval())

    def get_list(self):
        return AlignedStore().get([self.get_key()])[self.get_key()].tolist()


class TA(Expr):
    def __init__(self, expr: Expr):
        super().__init__(expr.get_interval())
        self.expr = expr

    def get_list(self):
        return self.calculate(pd.Series(self.expr.get_list())).tolist()

    @abstractmethod
    def calculate(self, data):
        raise NotImplementedError()


class SMA(TA):
    def __init__(self, expr: Expr, length: int):
        super().__init__(expr)
        self.length = length

    def calculate(self, data):
        return talib.SMA(data, self.length)


class STDDEV(TA):
    def __init__(self, expr: Expr, length: int):
        super().__init__(expr)
        self.length = length

    def calculate(self, data):
        return talib.STDDEV(data, self.length)
