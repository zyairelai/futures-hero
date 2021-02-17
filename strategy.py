import config
import entry_exit
import heikin_ashi
import pencil_wick
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

def dead_or_alive():
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = heikin_ashi.get_clear_direction()
    else: direction = heikin_ashi.get_hour(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)
    exit_minute  = heikin_ashi.exit_minute()

    if position_info == "LONGING":
        if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(exit_minute)) or entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if direction == "GREEN":
            if entry_exit.GO_LONG(one_minute, five_minute) and (one_hour != "RED" and not (pencil_wick.one_hour_test("RED"))):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED":
            if entry_exit.GO_SHORT(one_minute, five_minute) and (one_hour != "GREEN" and not (pencil_wick.one_hour_test("GREEN"))):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def fomo():
    position_info = get_position.get_position_info()
    six_hour     = heikin_ashi.get_hour(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)
    exit_minute  = heikin_ashi.exit_minute()

    if position_info == "LONGING":
        if entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour) or \
           ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or \
           ((six_hour == "RED") and ((one_hour == "RED") or (one_hour == "INDECISIVE")) and pencil_wick.one_hour_test("RED")):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour) or \
           ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(exit_minute)) or \
           ((six_hour == "GREEN") and ((one_hour == "GREEN") or (one_hour == "INDECISIVE")) and pencil_wick.one_hour_test("GREEN")):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if six_hour != "INDECISIVE":

            if entry_exit.GO_LONG(one_minute, five_minute) and (one_hour != "RED" and not (pencil_wick.one_hour_test("RED"))):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", config.quantity)

            elif entry_exit.GO_SHORT(one_minute, five_minute) and (one_hour != "GREEN" and not (pencil_wick.one_hour_test("GREEN"))):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", config.quantity)

            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
