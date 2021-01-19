import time
import config
from keys import client

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    positionAmt = float(client.futures_position_information(symbol=config.pair, timestamp=int(time.time()*1000))[0].get('positionAmt'))
    if (positionAmt > 0):   position = "LONGING"
    elif (positionAmt < 0): position = "SHORTING"
    else: position = "NO_POSITION"
    print("Current Position :   " + position)
    return position