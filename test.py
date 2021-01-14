import os
import time
import requests
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException

symbol   = "BTCUSDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_symbol():
    return "BTC" + "USDT"

def get_timestamp():
    return int(time.time() * 1000)

def output_exception(e):
    with open("Error_Message.txt", "a") as error_message:
        error_message.write("[!] " + get_symbol() + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
        error_message.write(e + "\n\n")

print(get_symbol())
print("Last action executed by " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    print(client.futures_position_information(symbol=get_symbol(), timestamp=get_timestamp(), recvWindow=1)[0])
except Exception as e:
    output_exception(str(e))
