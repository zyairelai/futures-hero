import os
import time
import requests
from binance.client import Client

symbol   = "BTCUSDT"
quantity = 0.001

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

position = client.futures_position_information(symbol=symbol, timestamp=get_timestamp(), recvWindow=5000)
print(position)

# scheduler = BlockingScheduler()
# scheduler.add_job(buy_low_sell_high, 'cron', second='0, 6, 12, 18, 24, 30, 36, 42, 48, 54')
# scheduler.start()

live_trade = True

if live_trade: print("True Live Trade")