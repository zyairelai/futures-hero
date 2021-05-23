import binance_futures_api, config, get_position
import direction, HA_current, HA_previous, place_order
from datetime import datetime
from termcolor import colored

throttle = config.throttle
live_trade = config.live_trade
enable_clear_direction = True

# ==========================================================================================================================================================================
#     Check on 1HR, 6HR, 12HR, entry on 1 minute. Zyaire's manual trading strategy for safer mode
# ==========================================================================================================================================================================

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)[0]
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    klines_12HOUR = binance_futures_api.KLINE_INTERVAL_12HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = get_position.profit_threshold()

    HA_current.output(mark_price, klines_12HOUR)
    HA_previous.output(klines_6HOUR)
    HA_current.output(mark_price, klines_6HOUR)
    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_1min)
    
    if throttle: leverage = config.leverage[i]
    else: leverage = int(config.leverage[i] + 10)
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if place_order.EXIT_LONG(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")

        elif place_order.THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures_api.throttle(i, "LONG")
            print("ACTION           :   🔥 THROTTLE_LONG 🔥")

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if place_order.EXIT_SHORT(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")

        elif place_order.THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures_api.throttle(i, "SHORT")
            print("ACTION           :   🔥 THROTTLE_SHORT 🔥")

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if enable_clear_direction:
            current_trend = direction.clear_direction(mark_price, klines_6HOUR)
        else: current_trend = direction.current_direction(mark_price, klines_6HOUR)

        if current_trend == "GREEN" and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            direction.current_direction(mark_price, klines_12HOUR) == "GREEN" and \
            place_order.GO_LONG_FOCUS(mark_price, klines_1min, klines_1HOUR):

            if live_trade: binance_futures_api.open_position(i, "LONG", config.quantity[i])
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif current_trend == "RED" and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            direction.current_direction(mark_price, klines_12HOUR) == "RED" and \
            place_order.GO_SHORT_FOCUS(mark_price, klines_1min, klines_1HOUR):

            if live_trade: binance_futures_api.open_position(i, "SHORT", config.quantity[i])
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
