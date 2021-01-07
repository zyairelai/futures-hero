import os
import time
from binance.client import Client

# start = time.time()
# print(f"Time Taken: {time.time() - start} seconds\n")

symbol  =  "BTCUSDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)

for k in klines:
    print(k)

position = client.futures_account_balance(timestamp=1591702613943)
print(position)