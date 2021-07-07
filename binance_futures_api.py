import os, time, config
from binance.client import Client
from termcolor import colored

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

def get_timestamp()              : return int(time.time() * 1000)
def timestamp_of(klines)         : return int(klines[-1][0])
def mark_price(i)                : return float(client.futures_mark_price(symbol=config.pair[i], timestamp=get_timestamp()).get('markPrice'))
def account_trades(i, timestamp) : return client.futures_account_trades(symbol=config.pair[i], timestamp=get_timestamp(), startTime=timestamp)
def change_leverage(i, leverage) : return client.futures_change_leverage(symbol=config.pair[i], leverage=leverage, timestamp=get_timestamp())
def change_margin_to_ISOLATED(i) : return client.futures_change_margin_type(symbol=config.pair[i], marginType="ISOLATED", timestamp=get_timestamp())
def change_margin_to_CROSSED(i)  : return client.futures_change_margin_type(symbol=config.pair[i], marginType="CROSSED", timestamp=get_timestamp())
def cancel_all_open_orders(i)    : return client.futures_cancel_all_open_orders(symbol=config.pair[i], timestamp=get_timestamp())
def get_open_orders(i)           : return client.futures_get_open_orders(symbol=config.pair[i], timestamp=get_timestamp())
def position_information(i)      : return client.futures_position_information(symbol=config.pair[i], timestamp=get_timestamp())[0]

query = 300
def KLINE_INTERVAL_1MINUTE(i)   : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_1MINUTE)
def KLINE_INTERVAL_3MINUTE(i)   : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_3MINUTE)
def KLINE_INTERVAL_5MINUTE(i)   : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_5MINUTE)
def KLINE_INTERVAL_15MINUTE(i)  : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_15MINUTE)
def KLINE_INTERVAL_30MINUTE(i)  : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_30MINUTE)
def KLINE_INTERVAL_1HOUR(i)     : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_2HOUR(i)     : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_2HOUR)
def KLINE_INTERVAL_4HOUR(i)     : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_4HOUR)
def KLINE_INTERVAL_6HOUR(i)     : return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_6HOUR)
def KLINE_INTERVAL_12HOUR(i)    : return client.get_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_12HOUR)

def initial_volume(klines)  : return float(klines[-4][5])
def firstrun_volume(klines) : return float(klines[-3][5])
def previous_volume(klines) : return float(klines[-2][5])
def current_volume(klines)  : return float(klines[-1][5])
def current_kline_timestamp(kline): return int(kline[-1][0])

def open_position(i, position, amount):
    if position == "LONG":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=amount, timestamp=get_timestamp())
        print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
    if position == "SHORT":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=amount, timestamp=get_timestamp())
        print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

def throttle(i, position):
    positionAmt = abs(float(position_information(i).get('positionAmt'))) * 2
    small_bites = config.quantity[i]
    if position == "LONG":
        if config.enable_throttle: 
            if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())
            print("ACTION           :   🔥 THROTTLE_LONG 🔥")
    if position == "SHORT":
        if config.enable_throttle: 
            if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())
            print("ACTION           :   🔥 THROTTLE_SHORT 🔥")

def close_position(i,position):
    positionAmt = float(position_information(i).get('positionAmt'))
    if position == "LONG":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
        print("ACTION           :   💰 CLOSE_LONG 💰")
    if position == "SHORT":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
        print("ACTION           :   💰 CLOSE_SHORT 💰")

# ==============================================================================================================================
#                                                   USELESS FUNCTIONS
# ==============================================================================================================================

round_decimal = 5

def set_trailing_stop(i, position, callbackRate):
    positionAmt = float(position_information(i).get('positionAmt'))
    if position == "LONG":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=abs(positionAmt), timestamp=get_timestamp())
    elif position == "SHORT":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, quantity=abs(positionAmt), timestamp=get_timestamp())

def set_take_profit(i, position, percentage): # Percentage to achieve so you could close the position
    positionAmt = float(position_information(i).get('positionAmt'))
    entryPrice = float(position_information(i).get("entryPrice"))
    liquidationPrice = float(position_information(i).get("liquidationPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice + ((liquidationPrice - entryPrice) * (percentage / 100))), round_decimal)
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        stopPrice = round((entryPrice - ((entryPrice - liquidationPrice) * (percentage / 100))), round_decimal)
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="TAKE_PROFIT_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

def set_stop_loss(i, position, percentage): # Percentage of the initial amount that you are willing to lose
    positionAmt = float(position_information(i).get('positionAmt'))
    entryPrice = float(position_information(i).get("entryPrice"))
    liquidationPrice = float(position_information(i).get("liquidationPrice"))

    if position == "LONG":
        stopPrice = round((entryPrice - ((entryPrice - liquidationPrice) * (percentage / 100))), round_decimal)
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())

    elif position == "SHORT":
        stopPrice = round((entryPrice + ((liquidationPrice - entryPrice) * (percentage / 100))), round_decimal)
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=abs(positionAmt), timeInForce="GTC", timestamp=get_timestamp())
