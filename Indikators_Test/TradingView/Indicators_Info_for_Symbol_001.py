from tradingview_ta import TA_Handler, Interval, Exchange
from pprint import pprint

handler = TA_Handler(
    symbol="LTCUSDT",
    screener="crypto",
    exchange="binance",
    interval=Interval.INTERVAL_1_DAY,
    # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
)
print(handler.get_analysis().summary)
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

pprint(handler.get_analysis().indicators)
