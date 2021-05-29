import os, time
from binance.client import Client

coin = input("\nEnter Coin Symbol (eg. BTC, ETH, BNB...) : ").upper()
trade_size_in_usdt = 1

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

def mark_price():
    return float(client.futures_mark_price(symbol=coin+"USDT", timestamp=get_timestamp()).get('markPrice'))

def leverage(coin):
    if   coin == "BTC": return 50
    elif coin == "ETH": return 40
    else: return 30

trade_amount_in_coin = round((trade_size_in_usdt * leverage(coin) / mark_price()), 6)
print("\nTrade Quantity in Coin : " + str(trade_amount_in_coin) + " " + coin)
print("\nThis would cost around : " + str(trade_size_in_usdt) + " USDT\n")
