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

client.futures_create_order(symbol=pair, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
client.futures_create_order(symbol=pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=0.1, quantity=quantity, timestamp=get_timestamp())

print(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0])