import os
import time
import config
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

# markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
# print(markPrice)

# stopPrice = round((markPrice - (markPrice * 0.15 / 100)), config.round_decimal)
# print(stopPrice)

# client.futures_create_order(symbol=config.pair, side="BUY", type="LIMIT", quantity=config.quantity, price=1.123, timestamp=get_timestamp(), timeInForce="GTC")

from datetime import datetime
if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
with open((os.path.join("Error_Message", config.pair + ".txt")), "a") as error_message:
    error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
    error_message.write("hehe" + "\n\n")
