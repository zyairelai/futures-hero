import os
import time
from binance.client import Client

# start = time.time()
# print(f"{time.time() - start} seconds\n")

symbol  =  "BTCUSDT"
bet     =  10

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")

candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)

for candle in candles:
    print(candle)

print(len(candle))