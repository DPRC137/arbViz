from .binance import BinanceConnector
from .bitget import BitgetConnector
from .bybit import BybitConnector
from .gateio import GateIOConnector
from .kraken import KrakenConnector
from .kucoin import KuCoinConnector
from .mexc import MEXCConnector
from .okx import OKXConnector


def connectors():
    return [
        BinanceConnector(), BybitConnector(), OKXConnector(), KrakenConnector(),
        KuCoinConnector(), GateIOConnector(), BitgetConnector(), MEXCConnector(),
    ]
