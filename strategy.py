use_stoploss = True
percentage = 20

import config
import entry_exit
import heikin_ashi
import pencil_wick
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

def dead_or_alive(CHILL_OR_FOMO):
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = heikin_ashi.get_clear_direction()
    else: direction = heikin_ashi.get_hour(6)
    five_minute   = heikin_ashi.get_current_minute(5)
    one_minute    = heikin_ashi.get_current_minute(1)
    exit_minute   = heikin_ashi.exit_minute()

    if position_info == "LONGING":
        if use_stoploss:
            if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("LONG", percentage)
            if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))
        else:
            if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT("LONG"):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if use_stoploss:
            if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("SHORT", percentage)
            if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(exit_minute)):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else: 
            if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT("SHORT"):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if CHILL_OR_FOMO == "FOMO" or CHILL_OR_FOMO == "fomo":
            if direction != "NO_TRADE_ZONE":
                if entry_exit.GO_LONG(one_minute, five_minute):
                    print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                    if config.live_trade: binance_futures.open_position("LONG")

                elif entry_exit.GO_SHORT(one_minute, five_minute):
                    print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                    if config.live_trade: binance_futures.open_position("SHORT")
                else: print("ACTION           :   🐺 WAIT 🐺")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: 
            if direction == "UP_TREND":
                if entry_exit.GO_LONG(one_minute, five_minute):
                    print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                    if config.live_trade: binance_futures.open_position("LONG")
                else: print("ACTION           :   🐺 WAIT 🐺")

            elif direction == "DOWN_TREND":
                if entry_exit.GO_SHORT(one_minute, five_minute):
                    print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                    if config.live_trade: binance_futures.open_position("SHORT")
                else: print("ACTION           :   🐺 WAIT 🐺")

            else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
