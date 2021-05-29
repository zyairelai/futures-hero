# Directons : Check on 1HR and 6HR, entry on 1 minute. 
# THE MOST STANDARD WAY (Zyaire's Manual Trading Strategy)

import backtest
import config
import direction
import get_position
import HA_current
import HA_previous
import place_order
import binance_futures_api
from datetime import datetime
from termcolor import colored

throttle = config.throttle
live_trade = config.live_trade
clear_direction = config.clear_direction

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)[0]
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = get_position.profit_threshold()

    HA_previous.output(klines_6HOUR)
    HA_current.output(mark_price, klines_6HOUR)
    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_1min)

    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)
    if not live_trade: backtest.trigger_backtest(i, mark_price, profit, klines_1min)

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
        if clear_direction: current_trend = direction.clear_direction(mark_price, klines_6HOUR)
        else: current_trend = direction.current_direction(mark_price, klines_6HOUR)

        if current_trend == "GREEN" and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            place_order.GO_LONG_FOCUS(mark_price, klines_1min, klines_1HOUR):
            OPEN_LONG_POSITION(i, mark_price)

        elif current_trend == "RED" and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            place_order.GO_SHORT_FOCUS(mark_price, klines_1min, klines_1HOUR):
            OPEN_SHORT_POSITION(i, mark_price)

        else: DO_NOTHING(i)
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def OPEN_LONG_POSITION(i, mark_price):
    if live_trade:
        binance_futures_api.open_position(i, "LONG", config.quantity[i])
        print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
    else: backtest.demo_long(i, mark_price)

def OPEN_SHORT_POSITION(i, mark_price):
    if live_trade:
        binance_futures_api.open_position(i, "SHORT", config.quantity[i])
        print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
    else: backtest.demo_short(i, mark_price)

def DO_NOTHING(i):
    if live_trade: print("ACTION           :   🐺 WAIT 🐺")
    else:
        if backtest.retrieve_position(i) == "NONE":
            print("ACTION           :   🐺 WAIT 🐺")
