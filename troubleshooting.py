import config
import direction
import HA_current
import place_order
import binance_futures_api

for i in range(len(config.pair)):
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_5min  = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
    klines_15min = binance_futures_api.KLINE_INTERVAL_15MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)

    ching_cheng_chong = HA_current.war_formation(mark_price, klines_1min)
    current_trend = direction.current_direction(mark_price, klines_6HOUR)

print(HA_current.war_formation(mark_price, klines_1min))
print(HA_current.heikin_ashi(mark_price, klines_1min) == "GREEN")
print(HA_current.heikin_ashi(mark_price, klines_5min)  == "GREEN")
print(HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN")
print(direction.clear_mini_direction_movement(klines_1HOUR))
