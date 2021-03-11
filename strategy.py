import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import current_candle
from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test
from heikin_ashi import strength_of_current
from heikin_ashi import one_minute_exit_test
from get_position import get_unRealizedProfit

live_trade = config.live_trade
# ==========================================================================================================================================================================
#                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================
def JACK_RABBIT():
    # RETRIEVE KLINES and INFORMATION
    position_info = get_position.get_position_info()
    klines_1min   = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_1HOUR  = binance_futures.KLINE_INTERVAL_1HOUR()
    klines_6HOUR  = binance_futures.KLINE_INTERVAL_6HOUR()
    
    # direction = heikin_ashi.get_clear_direction(6)
    direction = heikin_ashi.output_current(klines_6HOUR)
    heikin_ashi.output_current(klines_1HOUR)
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
        if (direction == "GREEN") and strength_of_current(klines_6HOUR) == "STRONG" and GO_LONG(klines_1HOUR, klines_1min):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if live_trade: binance_futures.open_position("LONG", trade_amount(klines_6HOUR, klines_1HOUR))

        elif (direction == "RED") and strength_of_current(klines_6HOUR) == "STRONG" and GO_SHORT(klines_1HOUR, klines_1min):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if live_trade: binance_futures.open_position("SHORT", trade_amount(klines_6HOUR, klines_1HOUR))
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def GO_LONG(klines_1HOUR, klines_1min):
    if (current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and \
       (strength_of_current(klines_1HOUR)  == "STRONG" and pattern_broken(klines_1HOUR) == "NOT_BROKEN")       and \
       (strength_of_current(klines_1min)   == "STRONG" and current_candle(klines_1min)  == "GREEN" and pencil_wick_test(klines_1min)) and \
        volume_confirmation(klines_1HOUR) : return True

def GO_SHORT(klines_1HOUR, klines_1min):
    if (current_candle(klines_1HOUR) == "RED"  or  current_candle(klines_1HOUR) == "RED_INDECISIVE")  and \
       (strength_of_current(klines_1HOUR)  == "STRONG" and pattern_broken(klines_1HOUR) == "NOT_BROKEN")      and \
       (strength_of_current(klines_1min)   == "STRONG" and current_candle(klines_1min)  == "RED" and pencil_wick_test(klines_1min)) and \
        volume_confirmation(klines_1HOUR) : return True

def EXIT_LONG(klines_1min):
    if one_minute_exit_test(klines_1min, "LONG"): return True

def EXIT_SHORT(klines_1min):
    if  one_minute_exit_test(klines_1min, "SHORT"): return True

def volume_confirmation(klines):
    return (binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) / 5))

def CUT_LOSS_LONG(six_hour):
    if six_hour != "GREEN": return True

def CUT_LOSS_SHORT(six_hour):
    if six_hour != "RED": return True

def DO_NOT_FUCKING_TRADE():
    return False

def slipping_back():
    return "Work in Progress"
# ==========================================================================================================================================================================
#                                                     Auto Adjusting Trade Amount
# ==========================================================================================================================================================================
def trade_amount(klines_6HOUR, klines_1HOUR):

    
    six = heikin_ashi.get_clear_direction(6)
    clear_six = (six == "GREEN" or six == "RED")

    one = heikin_ashi.get_clear_direction(1)
    clear_one = (one == "GREEN" or one == "RED")

    middle_finger_six = binance_futures.current_volume(klines_6HOUR) > binance_futures.previous_volume(klines_6HOUR)
    middle_finger_one = binance_futures.current_volume(klines_1HOUR) > binance_futures.previous_volume(klines_1HOUR)

    if clear_six and clear_one and middle_finger_six and middle_finger_one: trade_amount = config.quantity * 3
    else: trade_amount = config.quantity * 1

    return trade_amount
