import os
import time
import requests
from datetime import datetime
from binance.client import Client

symbol   = "BTCUSDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_symbol():
    main_coin = "BTC"
    return (main_coin + "USDT")

def get_timestamp():
    return int(time.time() * 1000)

# scheduler = BlockingScheduler()
# scheduler.add_job(buy_low_sell_high, 'cron', second='0, 6, 12, 18, 24, 30, 36, 42, 48, 54')
# scheduler.start()

print(get_symbol())
print("Last action executed by " + datetime.now().strftime("%H:%M:%S") + "\n")