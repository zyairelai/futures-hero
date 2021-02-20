import config
import entry_exit
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import silent_candle
from trade_amount import calculate_trade_amount

def dead_or_alive():
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = heikin_ashi.get_clear_direction()
    else: direction = heikin_ashi.get_hour(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if direction == "GREEN":
            if entry_exit.GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", calculate_trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED":
            if entry_exit.GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", calculate_trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def ultra_safe_mode():
    position_info = get_position.get_position_info()
    direction    = heikin_ashi.get_clear_direction()
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        first_six    = silent_candle("6HOUR", "FIRST")
        previous_six = silent_candle("6HOUR", "PREVIOUS")
        current_six  = silent_candle("6HOUR", "CURRENT")
        if (first_six != "GREEN") and (previous_six == "GREEN") and (current_six == "GREEN"): six_hour = "SAFE"
        elif (first_six != "RED") and (previous_six == "RED") and (current_six == "RED"): six_hour = "SAFE"
        else: six_hour = "NOT_SURE"

        first_one    = silent_candle("1HOUR", "FIRST")
        previous_one = silent_candle("1HOUR", "PREVIOUS")
        current_one  = silent_candle("1HOUR", "CURRENT")
        if (first_one != "GREEN") and (previous_one == "GREEN") and (current_one == "GREEN"): one_hour = "SAFE"
        elif (first_one != "RED") and (previous_one == "RED") and (current_one == "RED"): one_hour = "SAFE"
        else: one_hour = "NOT_SURE"

        if six_hour == "SAFE" and one_hour == "SAFE": mode = "SAFE"
        elif six_hour == "SAFE" and one_hour == "NOT_SURE": mode = "MODERATE"
        else: mode = "NOT_SURE"

        if direction == "GREEN" and mode == "SAFE":
            if entry_exit.GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED" and mode == "SAFE":
            if entry_exit.GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
