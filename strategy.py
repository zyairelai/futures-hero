import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import strength_of
from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test
from heikin_ashi import one_minute_exit_test
from get_position import get_unRealizedProfit

live_trade = config.live_trade
# ==========================================================================================================================================================================
#                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================
def JACK_RABBIT():
    position_info = get_position.get_position_info()
    # direction     = heikin_ashi.get_clear_direction()
    direction       = heikin_ashi.get_hour(6)
    one_hour      = heikin_ashi.get_hour(1)
    one_minute    = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_LONG():
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_SHORT():
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (direction == "GREEN") and strength_of("6HOUR") == "STRONG" and GO_LONG(one_hour, one_minute):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if live_trade: binance_futures.open_position("LONG", trade_amount())

        elif (direction == "RED") and strength_of("6HOUR") == "STRONG" and GO_SHORT(one_hour, one_minute):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if live_trade: binance_futures.open_position("SHORT", trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                  STRIFING - THIS ATTACK BOTH DIRECTION
# ==========================================================================================================================================================================
def STRIFING():
    position_info = get_position.get_position_info()
    one_hour      = heikin_ashi.get_hour(1)
    one_minute    = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_LONG():
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if get_unRealizedProfit() == "PROFIT" and EXIT_SHORT():
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and GO_LONG(one_hour, one_minute):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if live_trade: binance_futures.open_position("LONG", trade_amount())

        elif (one_hour == "RED" or one_hour == "RED_INDECISIVE") and GO_SHORT(one_hour, one_minute):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if live_trade: binance_futures.open_position("SHORT", trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def GO_LONG(one_hour, one_minute):
    if  (one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and volume_confirmation("1HOUR") and \
        (strength_of("1HOUR")   == "STRONG" and pattern_broken("1HOUR") == "NOT_BROKEN") and \
        (strength_of("1MINUTE") == "STRONG" and one_minute == "GREEN" and pencil_wick_test("GREEN")): return True

def GO_SHORT(one_hour, one_minute):
    if  (one_hour == "RED" or one_hour == "RED_INDECISIVE") and volume_confirmation("1HOUR") and \
        (strength_of("1HOUR")   == "STRONG" and pattern_broken("1HOUR") == "NOT_BROKEN") and \
        (strength_of("1MINUTE") == "STRONG" and one_minute == "RED" and pencil_wick_test("RED")): return True

def EXIT_LONG():
    if one_minute_exit_test("LONG"): return True

def EXIT_SHORT():
    if  one_minute_exit_test("SHORT"): return True

def volume_confirmation(INTERVAL):
    previous_volume = binance_futures.get_volume("PREVIOUS", INTERVAL)
    current_volume = binance_futures.get_volume("CURRENT", INTERVAL)
    return (current_volume > (previous_volume / 5))

def slipping_back():
    return "Work in Progress"
# ==========================================================================================================================================================================
#                                                     Auto Adjusting Trade Amount
# ==========================================================================================================================================================================
def trade_amount():
    six = heikin_ashi.get_clear_direction(6)
    clear_six = (six == "GREEN" or six == "RED")

    one = heikin_ashi.get_clear_direction(1)
    clear_one = (one == "GREEN" or one == "RED")

    previous_six = binance_futures.get_volume("PREVIOUS", "6HOUR")
    current_six  = binance_futures.get_volume("CURRENT",  "6HOUR")
    middle_finger_six = current_six > previous_six

    previous_one = binance_futures.get_volume("PREVIOUS", "1HOUR")
    current_one  = binance_futures.get_volume("CURRENT",  "1HOUR")
    middle_finger_one = current_one > previous_one

    if clear_six and clear_one and middle_finger_six and middle_finger_one: trade_amount = config.quantity * 3
    else: trade_amount = config.quantity * 1

    return trade_amount
