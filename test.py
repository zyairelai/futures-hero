pair = "ETHUSDT"
quantity = 0.001

import os
import time
import socket
import requests
import urllib3
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
def get_timestamp(): return int(time.time() * 1000)

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

# orderlist = [{'symbol' : pair, 'side' : "BUY", 'type' : "MARKET", 'quantity' : quantity},
#             {'symbol' : pair, 'side' : "SELL", 'type' : "TRAILING_STOP_MARKET", 'callbackRate' : 0.3, 'quantity' : quantity}]  
# payload = {'batchOrders':orderlist, 'timestamp': get_timestamp()}
# r = requests.post('https://fapi.binance.com/fapi/v1/batchOrders', params=payload)
# print (r.text)

print(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0])

"""
[!] BTCUSDT - Created at : 16-01-2021 @ 18:00:09
APIError(code=-1111): Precision is over the maximum defined for this asset.
"""