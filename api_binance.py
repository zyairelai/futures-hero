import os, time, config
from binance.client import Client
from termcolor import colored

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

def get_timestamp():
    return int(time.time() * 1000)

def position_information(pair):
    return client.futures_position_information(symbol=pair, timestamp=get_timestamp())

def account_trades(pair, timestamp) :
    return client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), startTime=timestamp)

def LONG_SIDE(response):
    if float(response[1].get('positionAmt')) > 0: return "LONGING"
    elif float(response[1].get('positionAmt')) == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if float(response[2].get('positionAmt')) < 0 : return "SHORTING"
    elif float(response[2].get('positionAmt')) == 0: return "NO_POSITION"

def change_leverage(pair, leverage):
    return client.futures_change_leverage(symbol=pair, leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(pair):
    return client.futures_change_margin_type(symbol=pair, marginType="ISOLATED", timestamp=get_timestamp())

def set_hedge_mode(): 
    if not client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="true", timestamp=get_timestamp())

def market_open_long(pair, quantity):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=quantity,
                                    positionSide="LONG",
                                    type="MARKET",
                                    side="BUY",
                                    timestamp=get_timestamp())
    print(colored("🚀 GO_LONG 🚀", "green"))

def market_open_short(pair, quantity):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=quantity,
                                    positionSide="SHORT",
                                    type="MARKET",
                                    side="SELL",
                                    timestamp=get_timestamp())
    print(colored("💥 GO_SHORT 💥", "red"))

def market_close_long(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=abs(float(response[1].get('positionAmt'))),
                                    positionSide="LONG",
                                    side="SELL",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("💰 CLOSE_LONG 💰")

def market_close_short(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=abs(float(response[2].get('positionAmt'))),
                                    positionSide="SHORT",
                                    side="BUY",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("💰 CLOSE_SHORT 💰")

set_hedge_mode()