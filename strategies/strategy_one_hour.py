# Strategy One Hour

import RSI
import MACD
import config
import candlestick
import get_position
import heikin_ashi
import hybrid
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    klines_4HOUR = binance_futures_api.KLINE_INTERVAL_4HOUR(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit_threshold = get_position.profit_threshold()

    rsi = RSI.current_RSI(candlestick.closing_price_list(klines_1HOUR))

    candlestick.output(klines_4HOUR)
    candlestick.output(klines_1HOUR)
    print()
    heikin_ashi.output(klines_4HOUR)
    heikin_ashi.output(klines_1HOUR)
    print("CURRENT 1HR RSI  :   " + str(rsi))

    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if EXIT_LONG(response, profit_threshold, klines_1HOUR): binance_futures_api.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, profit_threshold, klines_1HOUR): binance_futures_api.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else: check_trade_condition(i, klines_4HOUR, klines_1HOUR, rsi)

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
    if not config.live_trade: print_entry_condition(klines_4HOUR, klines_1HOUR, rsi)

def check_trade_condition(i, klines_4HOUR, klines_1HOUR, rsi):
    if GO_LONG(klines_4HOUR, klines_1HOUR, rsi): binance_futures_api.open_position(i, "LONG", config.quantity[i])
    elif GO_SHORT(klines_4HOUR, klines_1HOUR, rsi): binance_futures_api.open_position(i, "SHORT", config.quantity[i])
    else: print("ACTION           :   🐺 WAIT 🐺")

def GO_LONG(klines_4HOUR, klines_1HOUR, rsi):
    if hybrid.strong_trend(klines_4HOUR) == "GREEN" and hybrid.strong_trend(klines_1HOUR) == "GREEN" and rsi < RSI.upper_limit(): return True

def GO_SHORT(klines_4HOUR, klines_1HOUR, rsi):
    if hybrid.strong_trend(klines_4HOUR) == "RED" and hybrid.strong_trend(klines_1HOUR) == "RED" and rsi > RSI.lower_limit(): return True

def EXIT_LONG(response, profit_threshold, klines_1HOUR):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if hybrid.both_color(klines_1HOUR) == "RED": return True

def EXIT_SHORT(response, profit_threshold, klines_1HOUR):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if hybrid.both_color(klines_1HOUR) == "GREEN": return True

def print_entry_condition(klines_4HOUR, klines_1HOUR, rsi):
    test_color = "GREEN".upper()
    print("4 HOUR YES") if hybrid.strong_trend(klines_4HOUR) == test_color else print("4 HOUR NO")
    print("1 HOUR YES") if hybrid.strong_trend(klines_1HOUR) == test_color else print("1 HOUR NO")
    print("1 HOUR RSI " + str(rsi))
    print()
