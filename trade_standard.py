clear_direction = True

import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_position import get_position_info
from get_clear_direction import get_clear_direction

def standard_main_hour():
    position_info = get_position_info()
    if clear_direction: direction = get_clear_direction(4)
    else: direction = get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

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
        if direction == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "DOWN_TREND":
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")