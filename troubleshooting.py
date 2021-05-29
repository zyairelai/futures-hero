import config
import direction
import HA_current
import HA_previous
import binance_futures_api

# for i in range(len(config.pair)):
#     mark_price   = binance_futures_api.mark_price(i)
#     klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
#     klines_5min  = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
#     klines_15min = binance_futures_api.KLINE_INTERVAL_15MINUTE(i)
#     klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
#     klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
#     klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)

#     ching_cheng_chong = HA_current.war_formation(mark_price, klines_1min)
#     current_trend = direction.current_direction(mark_price, klines_6HOUR)
#     print(current_trend)

klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(0)

def candlebody_bigger_than_previous_wick(klines):
    return HA_current.candlebody(klines) > HA_previous.direction_wick(klines)

print(candlebody_bigger_than_previous_wick(klines_6HOUR))
print(HA_current.candlebody_bigger_than_previous_wick(klines_6HOUR))
