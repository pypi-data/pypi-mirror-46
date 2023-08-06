class Currency():
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Currencies():
    BTC = Currency('BTC')
    ETH = Currency('ETH')
    USDT = Currency('USDT')
    USD = Currency('USD')
    EOS = Currency('EOS')
    XRP = Currency('XRP')

    @staticmethod
    def get_currency(name: str):
        if name == 'BTC':
            return Currencies.BTC
        elif name == 'ETH':
            return Currencies.ETH
        elif name == 'EOS':
            return Currencies.EOS
        elif name == 'XRP':
            return Currencies.XRP
        elif name == 'USD':
            return Currencies.USD
        elif name == 'USDT':
            return Currencies.USDT
        else:
            return NotImplemented
