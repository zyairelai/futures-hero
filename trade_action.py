title           = "ACTION           :   "
import binance_futures
from datetime import datetime
from termcolor import colored
from get_trend import get_current_trend
from get_minute import get_current_minute
from get_position import get_position_info
from pencil_wick import pencil_wick_test

print()
prompt_LIVE = input("Enable Live Trade? [Y/n] ")
if prompt_LIVE == 'Y': 
    live_trade = True
    print(colored("Live Trade Enabled", "green"))
else: live_trade = False
prompt_TSL = input("Enable Trailing Stop? [Y/n] ")
if prompt_TSL == 'Y': 
    trailing_stop = True
    print(colored("Trailing Stop Enabled", "green"))
else: trailing_stop = False
print()

def minute_trade():
    position_info   = get_position_info()
    trend           = get_current_trend() # Get the Entry condition
    
    if position_info == "LONGING":
        minute_candle   = get_current_minute("EXIT")
        if (minute_candle == "RED") or (pencil_wick_test("GREEN") == "FAIL"):
            print(title + "💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored(title + "HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        minute_candle   = get_current_minute("EXIT")
        if (minute_candle == "GREEN") or (pencil_wick_test("RED") == "FAIL"):
            print(title + "💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored(title + "HOLDING_SHORT", "red"))

    else:
        minute_candle   = get_current_minute("YOU_KNOW_I_GO_GET")
        if trend == "UP_TREND":
            if (minute_candle == "GREEN") and (pencil_wick_test("GREEN") == "PASS"):
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
                if live_trade: 
                    binance_futures.open_position("LONG")
                    if trailing_stop: binance_futures.set_trailing_stop("LONG")
            else: print(title + "🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED") and (pencil_wick_test("RED") == "PASS"):
                print(colored(title + "💥 GO_SHORT 💥", "red"))
                if live_trade: 
                    binance_futures.open_position("SHORT")
                    if trailing_stop: binance_futures.set_trailing_stop("SHORT")
            else: print(title + "🐺 WAIT 🐺")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

