import api
import time
import requests
from binance.client import Client

# start = time.time()
# print(f"Time Taken: {time.time() - start} seconds\n")

symbol  =  "BTCUSDT"

# Get environment variables
# api_key     = os.environ.get('API_KEY')
# api_secret  = os.environ.get('API_SECRET')
api_key     = api.get_key()
api_secret  = api.get_secret()
client      = Client(api_key, api_secret)

timestamp = float(client.futures_time()["serverTime"])
print(timestamp)

# payload = {'timestamp': get_timestamp()}
# r = requests.get('https://fapi.binance.com/fapi/v2/balance', params=payload)
# print (r.text)

def get_timestamp():
    return int(time.time() * 1000)

position = client.futures_account_balance(timestamp=get_timestamp())
print(position)

mark_price = client.futures_mark_price(symbol=symbol)
print(mark_price)