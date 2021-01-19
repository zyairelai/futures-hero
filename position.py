import time
import config
from keys import client
def get_timestamp(): return int(time.time() * 1000)

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    positionAmt = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('positionAmt'))
    if (positionAmt > 0):   position = "LONGING"
    elif (positionAmt < 0): position = "SHORTING"
    else: position = "NO_POSITION"
    print("Current Position :   " + position)
    return position