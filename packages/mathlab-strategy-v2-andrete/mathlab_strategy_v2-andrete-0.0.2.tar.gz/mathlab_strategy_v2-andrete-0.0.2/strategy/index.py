from .currency import Currency, Currencies
from .ticker import Spot
from .exchange import Exchanges


class IndexVendor():
    def __init__(self, name: str):
        self.name = name


class IndexVendors():
    OKEx = IndexVendor('okex')


class Index():
    def __init__(self, weights: dict, base: Currency, vendor: IndexVendor):
        self.weights = weights
        self.base = base
        self.vendor = vendor


class Indices():
    BTCUSD = Index(
        {Spot(Currencies.BTC, Exchanges.Kraken): 1},
        Currencies.USD, IndexVendors.OKEx
    )
    ETHUSD = Index(
        {Spot(Currencies.ETH, Exchanges.Kraken): 1},
        Currencies.USD, IndexVendors.OKEx
    )
    EOSUSD = Index(
        {Spot(Currencies.EOS, Exchanges.Kraken): 1},
        Currencies.USD, IndexVendors.OKEx
    )
    XRPUSD = Index(
        {Spot(Currencies.XRP, Exchanges.Kraken): 1},
        Currencies.USD, IndexVendors.OKEx
    )
