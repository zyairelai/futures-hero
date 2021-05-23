import binance_futures_api
from HA_current import candle_size


klines_12HOUR = binance_futures_api.KLINE_INTERVAL_12HOUR(0)
klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(0)

print(candle_size(klines_12HOUR))