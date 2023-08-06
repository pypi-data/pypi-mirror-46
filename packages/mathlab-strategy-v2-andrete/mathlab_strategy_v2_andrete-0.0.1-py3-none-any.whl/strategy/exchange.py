class Exchange():
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Exchanges():
    Binance = Exchange('binance')
    Kraken = Exchange('kraken')
    OKEX = Exchange('okex')
