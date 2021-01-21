import time
import config
from keys import client
from termcolor import colored
def get_timestamp(): return int(time.time() * 1000)

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    positionAmt = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp)[0].get('positionAmt'))
    if (positionAmt > 0):
        position = "LONGING"
        print(colored("CURRENT POSITION :   " + position, "green"))
    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored("CURRENT POSITION :   " + position, "red"))
    else:
        position = "NO_POSITION"
        print("CURRENT POSITION :   " + position)
    return position
