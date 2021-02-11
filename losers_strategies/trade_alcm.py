# ALCM: Dead or Alive. Either you get liquidated or you hodl till you win. This is the highest winrate yet, HIGHEST RISK
use_stoploss = False    # ALCM is meant to NOT using any stoploss, so always False. If really want to use stoploss: 
stoploss = 100          # Percentage that you are willing to lose, in ALCM the stoploss cannot be less than 70% @50x leverage

import config
import entry_exit
import get_hour
import get_minute
import get_position
import get_clear_direction
import binance_futures
from datetime import datetime
from termcolor import colored

def dead_or_alive():
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = get_clear_direction.clear_direction()
    else: direction = get_hour.get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    exit_minute   = get_minute.exit_minute()

    if position_info == "LONGING":
        if use_stoploss:
            if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("LONG", stoploss)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if use_stoploss:
            if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("SHORT", stoploss)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(exit_minute):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
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
