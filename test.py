pair = "BTCUSDT"
quantity = 0.001

import os
import time
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

# RealizedPNL
# print(client.futures_position_information(symbol=pair, timestamp=get_timestamp()))
# trades = client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), limit=2)
# for each in trades:
#     print(each)
#     print("\n")

markPrice = float(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0].get('markPrice'))
print(markPrice)

stopPrice = round((markPrice - (markPrice * 0.15 / 100)), 2)
print(stopPrice)