import config
import time
from keys import client
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

def place_order(position):
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
        stopPrice = round((markPrice - (markPrice * config.stoplimit / 100)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
        stopPrice = round((markPrice + (markPrice * config.stoplimit / 100)), (config.round_decimal - 1))
        client.futures_create_order(symbol=config.pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())

def set_trailing_stop(position):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=config.callbackRate, quantity=config.quantity, timestamp=get_timestamp())
    elif position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=config.callbackRate, quantity=config.quantity, timestamp=get_timestamp())

