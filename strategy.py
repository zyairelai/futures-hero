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
#                                       JACK_RABBIT - IN AND OUT QUICK, CONSTANT GET YOU LIQUIDATED BUT YOU WILL NEVER GET WIPED OUT
# ==========================================================================================================================================================================
def JACK_RABBIT():
    position_info = get_position.get_position_info()
    six_hour      = heikin_ashi.get_hour(6)
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
        if (six_hour == "GREEN") and GO_LONG(one_hour, one_minute):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if live_trade: binance_futures.open_position("LONG", config.quantity)

        elif (six_hour == "RED") and GO_SHORT(one_hour, one_minute):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                                     ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def GO_LONG(one_hour, one_minute):
    if  strength_of("6HOUR") == "STRONG" and one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE" and \
        strength_of("1HOUR") == "STRONG" and pattern_broken("1HOUR") == "NOT_BROKEN" and \
        one_minute == "GREEN" and pencil_wick_test("GREEN") and \
        volume_confirmation("1HOUR"): return True

def GO_SHORT(one_hour, one_minute):
    if  strength_of("6HOUR") == "STRONG" and one_hour == "RED" or one_hour == "RED_INDECISIVE" and \
        strength_of("1HOUR") == "STRONG" and pattern_broken("1HOUR") == "NOT_BROKEN" and \
        one_minute == "GREEN" and pencil_wick_test("RED") and \
        volume_confirmation("1HOUR"): return True

def EXIT_LONG():
    if one_minute_exit_test("LONG") and volume_confirmation("1MINUTE"): return True

def EXIT_SHORT():
    if  one_minute_exit_test("SHORT") and volume_confirmation("1MINUTE"): return True

def volume_confirmation(INTERVAL):
    previous_volume = binance_futures.get_volume("PREVIOUS", INTERVAL)
    current_volume = binance_futures.get_volume("CURRENT", INTERVAL)
    return (current_volume > (previous_volume / 5))
