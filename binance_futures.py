import os
import time
import config
from binance.client import Client

# Get environment variables
api_owner   = os.environ.get('API_OWNER')
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

def account_trades(trades):
    return client.futures_account_trades(symbol=config.pair, timestamp=get_timestamp(), limit=(trades*2))

def change_leverage():
    return client.futures_change_leverage(symbol=config.pair, leverage=config.leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED():
    return client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp())

def cancel_all_open_orders():
    return client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())

def get_open_orders():
    return client.futures_get_open_orders(symbol=config.pair, timestamp=get_timestamp())

def position_information():
    return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())

def KLINE_INTERVAL_1MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=4)

def KLINE_INTERVAL_3MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_3MINUTE, limit=4)

def KLINE_INTERVAL_5MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE, limit=4)

def KLINE_INTERVAL_15MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_15MINUTE, limit=4)

def KLINE_INTERVAL_30MINUTE():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_30MINUTE, limit=4)

def KLINE_INTERVAL_1HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=4)

def KLINE_INTERVAL_2HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_2HOUR, limit=4)

def KLINE_INTERVAL_4HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=4)

def KLINE_INTERVAL_6HOUR():
    return client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=4)

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

def set_trailing_stop(position):
    callbackRate = 3
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=config.quantity, timestamp=get_timestamp())
    elif position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=config.quantity, timestamp=get_timestamp())

def set_take_profit(position, percentage): # Percentage to achieve so you could close the position
    entryPrice = float(position_information()[0].get("entryPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice + (entryPrice * percentage / 10000)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

    # Need to recheck the shorting price when in bearish market
    elif position == "SHORT":
        stopPrice = round((entryPrice - (entryPrice * percentage / 10000)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="BUY", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

def set_stop_loss(position, percentage): # Percentage of the initial amount that you are willing to lose
    entryPrice = float(position_information()[0].get("entryPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice - (entryPrice * percentage / 10000)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

    # Need to recheck the shorting price when in bearish market
    elif position == "SHORT":
        stopPrice = round((entryPrice + (entryPrice * percentage / 10000)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())
