import os
import time
import numpy as np
from binance.client import Client

# start = time.time()
# print(f"{time.time() - start} seconds\n")

symbol  =  "BTCUSDT"
bet     =  10
previous, current, temp = [], [], []

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "2 minute ago UTC")
previous_Time   = int(previous_klines[0][0])
previous_Open   = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
previous_Close  = round(((float(previous_klines[0][1]) + float(previous_klines[0][2]) + float(previous_klines[0][3]) + float(previous_klines[0][4])) / 4), 2)
previous_High   = max(float(previous_klines[0][2]), previous_Open, previous_Close)
previous_Low    = min(float(previous_klines[0][3]), previous_Open, previous_Close)

current_klines  = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
current_Time    = int(current_klines[0][0])
current_Open    = round(((previous_Open + previous_Close) / 2), 2)
current_Close   = round(((float(current_klines[0][1]) + float(current_klines[0][2]) + float(current_klines[0][3]) + float(current_klines[0][4])) / 4), 2)
current_High    = max(float(current_klines[0][2]), current_Open, current_Close)
current_Low     = min(float(current_klines[0][3]), current_Open, current_Close)

print(current_klines)