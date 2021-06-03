color = "RED"

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

print("BIG CANDLE       :   " + str(HA_current.candlebody_bigger_than_previous_candle(klines_1HOUR)))
print("SURPASS WICK     :   " + str(HA_current.candlebody_bigger_than_current_wick(klines_1HOUR)))

print("1 HOUR           :   " + str(HA_current.heikin_ashi(mark_price, klines_1HOUR) == color))
print("5 MINUTE         :   " + str(HA_current.heikin_ashi(mark_price, klines_5min)  == color))
print("1 MINUTE         :   " + str(HA_current.heikin_ashi(mark_price, klines_1min) == color))
print("WAR FORMATION    :   " + str(HA_current.war_formation(mark_price, klines_1min)))
