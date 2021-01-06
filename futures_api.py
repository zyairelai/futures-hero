import os
import time
import json
import requests
from binance.client import Client

symbol  =  "BTCUSDT"
bet     =  10

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

mark_price = client.futures_mark_price(symbol=symbol)
print(mark_price)

payload = {'symbol': symbol}
r = requests.get('https://fapi.binance.com/fapi/v2/positionRisk', params=payload)
print (r.text)