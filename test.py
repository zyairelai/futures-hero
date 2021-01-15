import os
import time
import socket
import requests
import urllib3
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
    realizedPnl = float(client.futures_account_trades(symbol=symbol, timestamp=get_timestamp())[-3].get('realizedPnl'))
except (BinanceAPIException, 
        ConnectionResetError, 
        socket.timeout,
        urllib3.exceptions.ProtocolError, 
        urllib3.exceptions.ReadTimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout) as e:
    output_exception(str(e))
else:
    print("whatever " + str(realizedPnl))