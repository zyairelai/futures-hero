import os
import time
import config
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp()             : return int(time.time() * 1000)
def account_trades(trades)      : return client.futures_account_trades(symbol=config.pair, timestamp=get_timestamp(), limit=(trades*2))
def change_leverage(leverage)   : return client.futures_change_leverage(symbol=config.pair, leverage=leverage, timestamp=get_timestamp())
def change_margin_to_ISOLATED() : return client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp())
def cancel_all_open_orders()    : return client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())
def get_open_orders()           : return client.futures_get_open_orders(symbol=config.pair, timestamp=get_timestamp())
def position_information()      : return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())

query = 4
def KLINE_INTERVAL_1MINUTE()    : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_1MINUTE)
def KLINE_INTERVAL_3MINUTE()    : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_3MINUTE)
def KLINE_INTERVAL_5MINUTE()    : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_5MINUTE)
def KLINE_INTERVAL_15MINUTE()   : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_15MINUTE)
def KLINE_INTERVAL_30MINUTE()   : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_30MINUTE)
def KLINE_INTERVAL_1HOUR()      : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_2HOUR()      : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_2HOUR)
def KLINE_INTERVAL_4HOUR()      : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_4HOUR)
def KLINE_INTERVAL_6HOUR()      : return client.futures_klines(symbol=config.pair, limit=query, interval=Client.KLINE_INTERVAL_6HOUR)
def KLINE_INTERVAL_12HOUR()     : return client.get_klines(symbol=config.pair, limit=4, interval=Client.KLINE_INTERVAL_12HOUR)

def get_volume(TIME_TRAVEL, INTERVAL):
    if   TIME_TRAVEL == "FIRSTRUN" : which = -3
    elif TIME_TRAVEL == "PREVIOUS" : which = -2
    elif TIME_TRAVEL == "CURRENT"  : which = -1
    if   INTERVAL == "1MINUTE"  : volume = KLINE_INTERVAL_1MINUTE()[which][5]
    elif INTERVAL == "3MINUTE"  : volume = KLINE_INTERVAL_3MINUTE()[which][5]
    elif INTERVAL == "5MINUTE"  : volume = KLINE_INTERVAL_5MINUTE()[which][5]
    elif INTERVAL == "15MINUTE" : volume = KLINE_INTERVAL_15MINUTE()[which][5]
    elif INTERVAL == "30MINUTE" : volume = KLINE_INTERVAL_30MINUTE()[which][5]
    elif INTERVAL == "1HOUR"    : volume = KLINE_INTERVAL_1HOUR()[which][5]
    elif INTERVAL == "2HOUR"    : volume = KLINE_INTERVAL_2HOUR()[which][5]
    elif INTERVAL == "4HOUR"    : volume = KLINE_INTERVAL_4HOUR()[which][5]
    elif INTERVAL == "6HOUR"    : volume = KLINE_INTERVAL_6HOUR()[which][5]
    return float(volume)

def open_position(position, amount):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=amount, timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=amount, timestamp=get_timestamp())

def close_position(position):
    positionAmt = float(position_information()[0].get('positionAmt'))
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())

def set_trailing_stop(position, callbackRate):
    positionAmt = float(position_information()[0].get('positionAmt'))
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=abs(positionAmt), timestamp=get_timestamp())
    elif position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=abs(positionAmt), timestamp=get_timestamp())

round_decimal = 5

def set_take_profit(position, percentage): # Percentage to achieve so you could close the position
    positionAmt = float(position_information()[0].get('positionAmt'))
    entryPrice = float(position_information()[0].get("entryPrice"))
    liquidationPrice = float(position_information()[0].get("liquidationPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice + ((liquidationPrice - entryPrice) * (percentage / 100))), round_decimal)
        client.futures_create_order(symbol=config.pair, side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        stopPrice = round((entryPrice - ((entryPrice - liquidationPrice) * (percentage / 100))), round_decimal)
        client.futures_create_order(symbol=config.pair, side="BUY", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

def set_stop_loss(position, percentage): # Percentage of the initial amount that you are willing to lose
    positionAmt = float(position_information()[0].get('positionAmt'))
    entryPrice = float(position_information()[0].get("entryPrice"))
    liquidationPrice = float(position_information()[0].get("liquidationPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice - ((entryPrice - liquidationPrice) * (percentage / 100))), round_decimal)
        client.futures_create_order(symbol=config.pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        stopPrice = round((entryPrice + ((liquidationPrice - entryPrice) * (percentage / 100))), round_decimal)
        client.futures_create_order(symbol=config.pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())
