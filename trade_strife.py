# Strife: Going both long && short when there is a clear direction
stoploss  = 40  # Percentage that you are willing to lose

import config
import entry_exit
import get_hour
import get_minute
import get_position
import get_clear_direction
import binance_futures
from datetime import datetime
from termcolor import colored

def strife_with_direction():
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = get_clear_direction.clear_direction()
    else: direction = get_hour.get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        if binance_futures.get_open_orders() == []: 
            if direction == "UP_TREND": binance_futures.set_stop_loss("LONG", stoploss)
            else: binance_futures.set_stop_loss("LONG", stoploss/2)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if binance_futures.get_open_orders() == []: 
            if direction == "DOWN_TREND": binance_futures.set_stop_loss("SHORT", stoploss)
            else: binance_futures.set_stop_loss("SHORT", stoploss/2)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if direction != "NO_TRADE_ZONE":
            if entry_exit.GO_LONG(one_minute, five_minute):
                if config.live_trade: binance_futures.open_position("LONG")
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif entry_exit.GO_SHORT(one_minute, five_minute):
                if config.live_trade: binance_futures.open_position("SHORT")
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
