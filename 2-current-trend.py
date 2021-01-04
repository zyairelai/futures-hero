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

previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "3 hour ago UTC")
previous_Time   = int(previous_klines[1][0])
previous_Open   = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
previous_Close  = round(((float(previous_klines[1][1]) + float(previous_klines[1][2]) + float(previous_klines[1][3]) + float(previous_klines[1][4])) / 4), 2)

print("The Initial Time is  :   " + str(previous_Time))
print("The Initial Open is  :   " + str(previous_Open))
print("The Initial Close is :   " + str(previous_Close) + "\n")

while True:
    current_klines  = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC")
    current_Time    = int(current_klines[0][0])

    if (current_Time - previous_Time) == 360000:
        temp_klines     = current_klines
        current_Open    = round(((previous_Open + previous_Close) / 2), 2)
        print("[>_<] previous open     : " + str(previous_Open))
        print("[>_<] previous close    : " + str(previous_Close))
        print("[>_<] current_Open      : " + str(current_Open) + "\n")
        current_Close   = round(((float(current_klines[0][1]) + float(current_klines[0][2]) + float(current_klines[0][3]) + float(current_klines[0][4])) / 4), 2)
        current_High    = max(float(current_klines[0][2]), current_Open, current_Close)
        current_Low     = min(float(current_klines[0][3]), current_Open, current_Close)
        
        print("The current_Time is  :   " + str(current_Time))
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low) + "\n")
    
    else:
        previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "3 hour ago UTC")
        previous_Time   = int(previous_klines[1][0])
        previous_Open   = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
        previous_Close  = round(((float(previous_klines[1][1]) + float(previous_klines[1][2]) + float(previous_klines[1][3]) + float(previous_klines[1][4])) / 4), 2)
        print("[^_^] New Candle")

    print("[+] Now Sleeping...\n")
    time.sleep(10)
