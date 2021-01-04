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

# Historical BLVT NAV Kline/Candlestick 
# https://binance-docs.github.io/apidocs/futures/en/#taker-buy-sell-volume
# [0] Open Timestamp            
# [1] Open                      HA_Open   = (previous HA_Open + previous HA_Close) / 2
# [2] High                      HA_Close  = (Open + High + Low + Close) / 4
# [3] Low                       HA_High   = maximum of High, HA_Open, HA_Close
# [4] Close                     HA_Low    = minimum of Low, HA_Open, HA_Close

previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "2 hour ago UTC")
previous.append(int(previous_klines[0][0])) # Timestamp
previous.append(round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)) # Open
previous.append(round(((float(previous_klines[0][1]) + float(previous_klines[0][2]) + float(previous_klines[0][3]) + float(previous_klines[0][4])) / 4), 2)) # Close
previous.append(max(float(previous_klines[0][2]), previous[1], previous[2])) # High
previous.append(min(float(previous_klines[0][3]), previous[1], previous[2])) # Low

previous_Time   = int(previous_klines[0][0])
previous_Open   = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
previous_Close  = round(((float(previous_klines[0][1]) + float(previous_klines[0][2]) + float(previous_klines[0][3]) + float(previous_klines[0][4])) / 4), 2)
previous_High   = max(float(previous_klines[0][2]), previous_Open, previous_Close)
previous_Low    = min(float(previous_klines[0][3]), previous_Open, previous_Close)

current_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC")
current.append(int(current_klines[0][0])) # Timestamp
current.append(round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)) # Open
current.append(round(((float(current_klines[0][1]) + float(current_klines[0][2]) + float(current_klines[0][3]) + float(current_klines[0][4])) / 4), 2)) # Close
current.append(max(float(current_klines[0][2]), current[1], current[2])) # High
current.append(min(float(current_klines[0][3]), current[1], current[2])) # Low

print(current)

while True:
    current_klines  = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC")
    current_Time    = int(current_klines[0][0])

    if (current_Time - previous_Time) == 3600000:
        current_Open  = round((previous_Open + previous_Close) / 2, 2)
        current_Close = round((float(current_klines[0][1]) + float(current_klines[0][2]) + float(current_klines[0][3]) + float(current_klines[0][4])) / 4, 2)
        current_High  = max(float(current_klines[0][2]), current_Open, current_Close)
        current_Low   = min(float(current_klines[0][3]), current_Open, current_Close)

        for current in current_klines:
            print(current)
    
    else:
        previous_Time = current_klines

    time.sleep(10)
