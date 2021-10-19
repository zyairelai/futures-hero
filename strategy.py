# Strategy Heikin Ashi

import RSI
import MACD
import config
import candlestick
import get_position
import heikin_ashi
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    klines_4HOUR = binance_futures_api.KLINE_INTERVAL_4HOUR(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_5MIN  = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
    klines_1MIN  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    position_info = get_position.get_position_info(i, response)
    profit_threshold = get_position.profit_threshold()

    rsi_5MIN = RSI.current_RSI(candlestick.closing_price_list(klines_5MIN))
    rsi_1MIN = RSI.current_RSI(candlestick.closing_price_list(klines_1MIN))

    heikin_ashi.output(klines_4HOUR)
    heikin_ashi.output(klines_1HOUR)
    heikin_ashi.output(klines_5MIN)
    heikin_ashi.output(klines_1MIN)
    print("CURRENT 5MIN RSI :   " + str(rsi_5MIN))
    print("CURRENT 1MIN RSI :   " + str(rsi_1MIN))

    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if EXIT_LONG(response, profit_threshold, klines_1MIN): binance_futures_api.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, profit_threshold, klines_1MIN): binance_futures_api.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else: check_trade_condition(i, klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN)

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
    if not config.live_trade: print_entry_condition(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN)

def check_trade_condition(i, klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
    if GO_LONG(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
        binance_futures_api.open_position(i, "LONG", config.quantity[i])
    elif GO_SHORT(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
        binance_futures_api.open_position(i, "SHORT", config.quantity[i])
    else: print("ACTION           :   🐺 WAIT 🐺")

def hot_zone(klines_30MIN, klines_1HOUR):
    if klines_1HOUR[-1][0] == klines_30MIN[-1][0]: return True

def GO_LONG(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
    if MACD.long_condition(klines_1MIN) and \
        heikin_ashi.VALID_CANDLE(klines_4HOUR) == "GREEN" and \
        heikin_ashi.VALID_CANDLE(klines_1HOUR) == "GREEN" and \
        heikin_ashi.VALID_CANDLE(klines_5MIN) == "GREEN" and \
        heikin_ashi.VALID_CANDLE(klines_1MIN) == "GREEN" and \
        rsi_5MIN < RSI.upper_limit() and rsi_1MIN < RSI.upper_limit(): return True

def GO_SHORT(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
    if MACD.short_condition(klines_1MIN) and \
        heikin_ashi.VALID_CANDLE(klines_4HOUR) == "RED" and \
        heikin_ashi.VALID_CANDLE(klines_1HOUR) == "RED" and \
        heikin_ashi.VALID_CANDLE(klines_5MIN) == "RED" and \
        heikin_ashi.VALID_CANDLE(klines_1MIN) == "RED" and \
        rsi_5MIN > RSI.lower_limit() and rsi_1MIN > RSI.lower_limit(): return True

def EXIT_LONG(response, profit_threshold, klines_1MIN):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if heikin_ashi.VALID_CANDLE(klines_1MIN) == "RED": return True

def EXIT_SHORT(response, profit_threshold, klines_1MIN):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if heikin_ashi.VALID_CANDLE(klines_1MIN) == "GREEN": return True

def print_entry_condition(klines_4HOUR, klines_1HOUR, klines_5MIN, klines_1MIN, rsi_5MIN, rsi_1MIN):
    print("4 HOUR", heikin_ashi.VALID_CANDLE(klines_4HOUR))
    print("1 HOUR", heikin_ashi.VALID_CANDLE(klines_1HOUR))
    print("5 MIN", heikin_ashi.VALID_CANDLE(klines_5MIN))
    print("1 MIN", heikin_ashi.VALID_CANDLE(klines_1MIN))
    if MACD.long_condition(klines_1MIN): print("MACD  LONG")
    if MACD.short_condition(klines_1MIN): print("MACD SHORT") 
    print("5MIN RSI " + str(rsi_5MIN))
    print("1MIN RSI " + str(rsi_1MIN))
    print()
