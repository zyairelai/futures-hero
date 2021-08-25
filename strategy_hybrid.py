import RSI
import config
import candlestick
import get_position
import hybrid
import heikin_ashi
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    main_direction    = binance_futures_api.KLINE_INTERVAL_4HOUR(i)
    support_direction = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    entry_interval    = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    position_info     = get_position.get_position_info(i, response)
    profit_threshold  = get_position.profit_threshold()

    closing_dataset = candlestick.closing_price_list(entry_interval)
    rsi = RSI.current_RSI(closing_dataset)

    heikin_ashi.output(main_direction)
    candlestick.output(main_direction)
    heikin_ashi.output(support_direction)
    candlestick.output(support_direction)
    heikin_ashi.output(entry_interval)
    print("CURRENT RSI      :   " + str(rsi))

    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if EXIT_LONG(response, profit_threshold, entry_interval): binance_futures_api.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, profit_threshold, entry_interval): binance_futures_api.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if GO_LONG(main_direction, support_direction, entry_interval, rsi): binance_futures_api.open_position(i, "LONG", config.quantity[i])
        elif GO_SHORT(main_direction, support_direction, entry_interval, rsi): binance_futures_api.open_position(i, "SHORT", config.quantity[i])
        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def GO_LONG(main_direction, support_direction, entry_interval, rsi):
    if  hybrid.strong_trend(main_direction) == "GREEN" and \
        hybrid.strong_trend(support_direction) == "GREEN" and \
        hybrid.strong_trend(entry_interval) == "GREEN" and \
        rsi < 70: return True

def GO_SHORT(main_direction, support_direction, entry_interval, rsi):
    if  hybrid.strong_trend(main_direction) == "RED" and \
        hybrid.strong_trend(support_direction) == "RED" and \
        hybrid.strong_trend(entry_interval) == "RED" and \
        rsi > 30: return True

def EXIT_LONG(response, profit_threshold, entry_interval):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if hybrid.strong_trend(entry_interval) == "RED": return True

def EXIT_SHORT(response, profit_threshold, entry_interval):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if hybrid.strong_trend(entry_interval) == "GREEN": return True
