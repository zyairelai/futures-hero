import time
import config
import binance_futures
from termcolor import colored

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = "CURRENT POSITION :   "
    positionAmt = float(binance_futures.position_information()[0].get('positionAmt'))

    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))

    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))

    else:
        position = "NO_POSITION"
        print(title + position)

    return position
