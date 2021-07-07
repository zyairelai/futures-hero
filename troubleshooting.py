color = "RED"

import config
import direction
import HA_current
import place_order
import binance_futures_api
from termcolor import colored

for i in range(len(config.pair)):
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)

    ching_cheng_chong = HA_current.war_formation(mark_price, klines_1min)
    current_trend = direction.current_direction(mark_price, klines_6HOUR)

    print("CURRET TREND     :   " + str(current_trend))
    print("IS NOW HOT ZONE  :   " + str(direction.hot_zone(klines_30MIN, klines_6HOUR)))
    print("ABS CLEAR DIR    :   " + str(direction.absolute_clear_direction(mark_price, klines_6HOUR)))
    print("CLEAR DIRECTION  :   " + str(direction.clear_direction(mark_price, klines_6HOUR)))

    print()
    print("1 HOUR           :   " + str(HA_current.heikin_ashi(mark_price, klines_1HOUR) == color))
    print("1 MINUTE         :   " + str(HA_current.heikin_ashi(mark_price, klines_1min) == color))
    print("WAR FORMATION    :   " + str(HA_current.war_formation(mark_price, klines_1min)))
    print()
    print(colored("LONG CONDITION   :   " + str(place_order.GO_LONG_EMA(mark_price, klines_1min, klines_1HOUR)), "green"))
    print(colored("SHORT CONDITION  :   " + str(place_order.GO_LONG_EMA(mark_price, klines_1min, klines_1HOUR)), "red"))
    print()
    print("BIG CANDLE       :   " + str(HA_current.candlebody_bigger_than_previous_candle(klines_1HOUR)))
    print("SURPASS WICK     :   " + str(HA_current.candlebody_bigger_than_current_wick(klines_1HOUR)))

    print(HA_current.candle_size(klines_6HOUR))
