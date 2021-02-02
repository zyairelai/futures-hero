import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_minute import emergency_minute
from get_position import get_position_info

def fomo_no_trend():
    position_info = get_position_info()
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = emergency_minute()

    if position_info == "LONGING":
        if (five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if (five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            binance_futures.open_position("LONG")
        elif (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            binance_futures.open_position("SHORT")
        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")