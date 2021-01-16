import os
import time
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

start = time.time()
pair  = "BTC" + "USDT"

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    position_response = client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0]
    positionAmt = float(position_response.get('positionAmt'))
    print(position_response)

    if (positionAmt > 0):
        position = "LONGING"
    elif (positionAmt < 0):
        position = "SHORTING"
    else:
        position = "NO_POSITION"
    print("Current Position :   " + position)
    return position

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

print("\nThe <position.py> return value is : " + get_position_info() + "\n")
print(f"Time Taken: {time.time() - start} seconds\n")
