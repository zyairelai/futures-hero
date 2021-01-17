pair = "LINK" + "USDT"
round_decimal = 4

import os
import time
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

# markPrice = float(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0].get('markPrice'))
# print(markPrice)

# stopPrice = round((markPrice - (markPrice * 0.15 / 100)), round_decimal)
# print(stopPrice)

client.futures_create_order(symbol=pair, side="BUY", type="LIMIT", quantity=1, price=1.123, timestamp=get_timestamp(), timeInForce="GTC")