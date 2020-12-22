import os
import time
from binance.client import Client

# start = time.time()
# print(f"{time.time() - start} seconds\n")

asset   = "BTC"
base    = "USDT"
symbol  =  asset + base
bet     =  10

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

