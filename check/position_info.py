import os
import time
from binance.client import Client

start   =   time.time()
symbol   = "BTCUSDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)  

def get_position_info():
    position_response = client.futures_position_information(symbol=symbol, timestamp=get_timestamp())[0]
    positionAmt = float(position_response.get('positionAmt'))
    print(position_response)
    
    if (positionAmt > 0):
        print("Current Position   :   LONGING")
        return "LONGING"
    elif (positionAmt < 0):
        print("Current Position   :   SHORTING")
        return "SHORTING"
    else:
        print("Current Position   :   NO_POSITION")
        return "NO_POSITION"

result = get_position_info()
print("\nThe <position.py> return value is : " + result + "\n")
print(f"Time Taken: {time.time() - start} seconds\n")