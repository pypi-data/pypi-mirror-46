from .common import Value


class MA(Value):
    def __init__(self, value: Value, length: int):
        super().__init__('ta_ma_%s_%d' % (value.get_key(), length))


class STD(Value):
    def __init__(self, value: Value, length: int):
        super().__init__('ta_std_%s_%d' % (value.get_key(), length))
