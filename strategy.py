# Strategy Heikin Ashi

import MACD
import config
import candlestick
import heikin_ashi
import get_position
import api_binanceusdm
import pandas as pd
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):

    # Retrieve Infomation for Initial Trade Setup
    response = api_binanceusdm.position_information(i)
    if response.get('marginType') != "isolated": api_binanceusdm.change_margin_to_ISOLATED(i)
    if int(response.get("leverage")) != config.leverage[i]: api_binanceusdm.change_leverage(i, config.leverage[i])

    # Retrieve Raw Candlestick Klines
    raw_6HOUR = candlestick.KLINE_INTERVAL_6HOUR(i)
    raw_1HOUR = candlestick.KLINE_INTERVAL_1HOUR(i)
    raw_1MIN  = candlestick.KLINE_INTERVAL_1MIN(i)

    # Process Heikin Ashi & Apply Technical Analysis
    ha_6HOUR = heikin_ashi.heikin_ashi(raw_6HOUR)
    ha_1HOUR = heikin_ashi.heikin_ashi(raw_1HOUR)
    ha_1MIN  = heikin_ashi.heikin_ashi(raw_1MIN)
    macd_1MIN = MACD.apply_default(raw_1MIN)

    # Console Output
    heikin_ashi.output(ha_6HOUR)
    heikin_ashi.output(ha_1HOUR)
    heikin_ashi.output(ha_1MIN)

    # Place Order Condition
    position_info = get_position.get_position_info(i, response)

    if position_info == "LONGING":
        if EXIT_LONG(response, ha_1MIN): api_binanceusdm.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, ha_1MIN): api_binanceusdm.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else: 
        if   GO_LONG (ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN): api_binanceusdm.open_position(i, "LONG" , config.quantity[i])
        elif GO_SHORT(ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN): api_binanceusdm.open_position(i, "SHORT", config.quantity[i])
        else: print("ACTION           :   🐺 WAIT 🐺")

    # Output Execution logs on Console
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
    if not config.live_trade: print_entry_condition(ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN)

# ==========================================================================================================================================================================
#                                                               CONDITION
# ==========================================================================================================================================================================

def hot_zone(raw_6HOUR, raw_30MIN):
    if raw_6HOUR['timestamp'].iloc[-1] == raw_30MIN['timestamp'].iloc[-1]: return True

def GO_LONG(ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN):
    if  ha_6HOUR["VALID"].iloc[-1] == "GREEN" and \
        ha_1HOUR["VALID"].iloc[-1] == "GREEN" and \
        ha_1MIN ["color"].iloc[-1] == "GREEN" and \
        ha_1MIN["strong"].iloc[-1] ==  True   and \
        macd_1MIN["long"].iloc[-1] ==  True: return True
    else: return False

def GO_SHORT(ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN):
    if  ha_6HOUR["VALID"].iloc[-1] == "GREEN" and \
        ha_1HOUR["VALID"].iloc[-1] == "GREEN" and \
        ha_1MIN ["color"].iloc[-1] == "GREEN" and \
        ha_1MIN["strong"].iloc[-1] ==  True   and \
        macd_1MIN["short"].iloc[-1] == True: return True
    else: return False

def EXIT_LONG(response, ha_1MIN):
    return True if get_position.profit_or_loss(response, config.profit_margin) == "PROFIT" and ha_1MIN ["color"].iloc[-1] == "RED" else False

def EXIT_SHORT(response, ha_1MIN):
    return True if get_position.profit_or_loss(response, config.profit_margin) == "PROFIT" and ha_1MIN ["color"].iloc[-1] == "GREEN" else False

# ==========================================================================================================================================================================
#                                                               TEST
# ==========================================================================================================================================================================

def print_entry_condition(ha_6HOUR, ha_1HOUR, ha_1MIN, macd_1MIN):
    print("6 HOUR", ha_6HOUR["VALID"].iloc[-1])
    print("1 HOUR", ha_1HOUR["VALID"].iloc[-1])
    print("1 MIN ", ha_1MIN ["color"].iloc[-1])
    print("_MACD  LONG") if macd_1MIN["long"].iloc[-1] else print("_MACD  WAIT")
    print("_MACD  SHORT") if macd_1MIN["short"].iloc[-1] else print("_MACD  WAIT")
    print()

def test(): lets_make_some_money(0)
# test()