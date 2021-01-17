import os
import time
import config
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    positionAmt = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('positionAmt'))
    if (positionAmt > 0):   position = "LONGING"
    elif (positionAmt < 0): position = "SHORTING"
    else: position = "NO_POSITION"
    print("Current Position :   " + position)
    return position

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

start = time.time()
print("\nThe <position.py> return value is : " + get_position_info())
print(f"Time Taken: {time.time() - start} seconds\n")
