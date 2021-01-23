import os
import time
import config
from binance.client import Client

stoplimit    = 0.2
callbackRate = 0.5

# Get environment variables
api_owner   = os.environ.get('API_OWNER')
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)
    
def position_information():
    return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp)

def change_leverage():
    return client.futures_change_leverage(symbol=config.pair, leverage=config.leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED():
    return client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp)

def cancel_all_open_orders():
    client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())

def account_trades(trades):
    return client.futures_account_trades(symbol=config.pair, timestamp=get_timestamp(), limit=(trades*2))

def KLINE_INTERVAL_1MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

def KLINE_INTERVAL_3MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_3MINUTE, limit=3)

def KLINE_INTERVAL_5MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE, limit=3)

def KLINE_INTERVAL_1HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)

def KLINE_INTERVAL_2HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_2HOUR, limit=3)

def KLINE_INTERVAL_4HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)

def KLINE_INTERVAL_6HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)

def open_position(position):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())

def close_position(position):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())

def set_stop_loss(position):
    if position == "LONG":
        markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
        stopPrice = round((markPrice - (markPrice * stoplimit / 100)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
        stopPrice = round((markPrice + (markPrice * stoplimit / 100)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

def set_trailing_stop(position):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=config.quantity, timestamp=get_timestamp())
    elif position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=config.quantity, timestamp=get_timestamp())
