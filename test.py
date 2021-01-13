import os
import time
import requests
from binance.client import Client

# start = time.time()
# print(f"Time Taken: {time.time() - start} seconds\n")

symbol   = "BTCUSDT"
quantity = 0.001

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)


# Success Long Order
# client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())

# Success Short Order
# client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())

position = client.futures_position_information(symbol=symbol, timestamp=get_timestamp())
print(position)
positionAmt = float(client.futures_position_information(symbol=symbol, timestamp=get_timestamp())[0].get('positionAmt'))
print(positionAmt)
if (positionAmt > 0):
    print("LONGING")
elif (positionAmt < 0):
    print("SHORTING")
else:
    print("NO_POSITION")

