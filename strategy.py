import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import strength_of
from heikin_ashi import current_candle
from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test
from heikin_ashi import one_minute_exit_test
from get_position import get_unRealizedProfit

live_trade = config.live_trade
# ==========================================================================================================================================================================
#                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================
def JACK_RABBIT():
    # RETRIEVE KLINES and INFORMATION
    position_info  = get_position.get_position_info()
    klines_1min    = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_1hr     = binance_futures.KLINE_INTERVAL_1HOUR()
    klines_6hr     = binance_futures.KLINE_INTERVAL_6HOUR()
    
    # direction = heikin_ashi.get_clear_direction(6)
    direction = heikin_ashi.output_current(klines_6hr)
    heikin_ashi.output_current(klines_1hr)
    heikin_ashi.output_current(klines_1min)

    if position_info == "LONGING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_LONG(klines_1min):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_SHORT(klines_1min):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (direction == "GREEN") and strength_of(klines_6hr) == "STRONG" and GO_LONG(klines_1hr, klines_1min):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if live_trade: binance_futures.open_position("LONG", trade_amount(klines_6hr, klines_1hr))

        elif (direction == "RED") and strength_of(klines_6hr) == "STRONG" and GO_SHORT(klines_1hr, klines_1min):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if live_trade: binance_futures.open_position("SHORT", trade_amount(klines_6hr, klines_1hr))
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def GO_LONG(klines_1hr, klines_1min):
    if (current_candle(klines_1hr) == "GREEN" or current_candle(klines_1hr)  == "GREEN_INDECISIVE") and \
       (strength_of(klines_1hr)  == "STRONG" and pattern_broken(klines_1hr)  == "NOT_BROKEN")       and \
       (strength_of(klines_1min) == "STRONG" and current_candle(klines_1min) == "GREEN" and pencil_wick_test("GREEN")) and \
        volume_confirmation(klines_1hr) : return True

def GO_SHORT(klines_1hr, klines_1min):
    if (current_candle(klines_1hr) == "RED"  or  current_candle(klines_1hr)  == "RED_INDECISIVE")  and \
       (strength_of(klines_1hr)  == "STRONG" and pattern_broken(klines_1hr)  == "NOT_BROKEN")      and \
       (strength_of(klines_1min) == "STRONG" and current_candle(klines_1min) == "RED" and pencil_wick_test("RED")) and \
        volume_confirmation(klines_1hr) : return True

def EXIT_LONG(klines_1min):
    if one_minute_exit_test(klines_1min, "LONG"): return True

def EXIT_SHORT(klines_1min):
    if  one_minute_exit_test(klines_1min, "SHORT"): return True

def volume_confirmation(klines):
    previous_volume = binance_futures.get_volume("PREVIOUS", klines)
    current_volume = binance_futures.get_volume("CURRENT", klines)
    return (current_volume > (previous_volume / 5))

def CUT_LOSS_LONG(six_hour):
    if six_hour != "GREEN": return True

def CUT_LOSS_SHORT(six_hour):
    if six_hour != "RED": return True

def slipping_back():
    return "Work in Progress"
# ==========================================================================================================================================================================
#                                                     Auto Adjusting Trade Amount
# ==========================================================================================================================================================================
def trade_amount(klines_6hr, klines_1hr):
    six = heikin_ashi.get_clear_direction(6)
    clear_six = (six == "GREEN" or six == "RED")

    one = heikin_ashi.get_clear_direction(1)
    clear_one = (one == "GREEN" or one == "RED")

    previous_six = binance_futures.get_volume("PREVIOUS", klines_6hr)
    current_six  = binance_futures.get_volume("CURRENT",  klines_6hr)
    middle_finger_six = current_six > previous_six

    previous_one = binance_futures.get_volume("PREVIOUS", klines_1hr)
    current_one  = binance_futures.get_volume("CURRENT",  klines_1hr)
    middle_finger_one = current_one > previous_one

    if clear_six and clear_one and middle_finger_six and middle_finger_one: trade_amount = config.quantity * 3
    else: trade_amount = config.quantity * 1

    return trade_amount
