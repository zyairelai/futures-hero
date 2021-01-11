import os
import time
import requests
from binance.client import Client

# start = time.time()
# print(f"Time Taken: {time.time() - start} seconds\n")

symbol  =  "BTCUSDT"

# Get environment variables
api_key     = "0b6bab25b86fe60215b90a805d919eb81a330652ec10624a661300449067d3e5"
api_secret  = "aafb5b1058ebbab777746ecce25d18606f66ab1f0234fa89129bfcd31d123d85"
client      = Client(api_key, api_secret)

timestamp = client.futures_time()["serverTime"]
print(timestamp) # Type int

# payload = {'timestamp': get_timestamp()}
# r = requests.get('https://fapi.binance.com/fapi/v2/balance', params=payload)
# print (r.text)

# position = client.futures_account_balance(timestamp=get_timestamp())
# print(position)

mark_price = client.futures_mark_price(symbol=symbol)
print(mark_price)