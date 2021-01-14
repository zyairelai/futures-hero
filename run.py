live_trade  = True

import os
import time
import socket
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_symbol():
    return "BTC" + "USDT"

def create_order(side):
    quantity    =   0.001
    # side  >>>  "BUY"      For >>> GO_LONG // CLOSE_SHORT
    # side  >>>  "SELL"     For >>> GO_SHORT // CLOSE_LONG
    client.futures_create_order(symbol=get_symbol(), side=side, type="MARKET", quantity=quantity, timestamp=get_timestamp())

def get_current_trend():
    klines = client.futures_klines(symbol=get_symbol(), interval=Client.KLINE_INTERVAL_2HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        trend = "DOWN_TREND"
        print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif (current_Open == current_Low):
        trend = "UP_TREND"
        print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def get_minute_candle():
    klines = client.futures_klines(symbol=get_symbol(), interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        minute_candle = "RED_CANDLE"
        print("Current MINUTE   :   🩸 RED 🩸")
    elif (current_Open == current_Low):
        minute_candle = "GREEN_CANDLE"
        print("Current MINUTE   :   🥦 GREEN 🥦")
    else:
        if (current_Open > current_Close):
            minute_candle = "RED_INDECISIVE"
            print("Current MINUTE   :   🩸 RED_INDECISIVE 🩸")
        elif (current_Close > current_Open):
            minute_candle = "GREEN_INDECISIVE"
            print("Current MINUTE   :   🥦 GREEN_INDECISIVE 🥦")
        else:
            minute_candle = "SOMETHING_IS_WRONG"
            print("❗SOMETHING_IS_WRONG in get_minute_candle()❗")
    return minute_candle

def get_position_info():
    positionAmt = float(client.futures_position_information(symbol=get_symbol(), timestamp=get_timestamp())[0].get('positionAmt'))
    if (positionAmt > 0):
        position = "LONGING"
    elif (positionAmt < 0):
        position = "SHORTING"
    else:
        position = "NO_POSITION"
    print("Current Position :   " + position)
    return position

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            if live_trade: create_order("SELL")             ### CREATE SELL ORDER HERE
            print("Action           :   CLOSE_LONG 😋")
        else:
            print("Action           :   HOLDING_LONG 💪🥦")

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            if live_trade: create_order("BUY")              ### CREATE BUY ORDER HERE
            print("Action           :   CLOSE_SHORT 😋")
        else:
            print("Action           :   HOLDING_SHORT 💪🩸")

    else:
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                if live_trade: create_order("BUY")          ### CREATE BUY ORDER HERE
                print("Action           :   GO_LONG 🚀")
            else:
                print("Action           :   WAIT 🐺")
        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                if live_trade: create_order("SELL")         ### CREATE SELL ORDER HERE
                print("Action           :   GO_SHORT 💥")
            else:
                print("Action           :   WAIT 🐺")
        else:
            print("Action           :   WAIT 🐺")

def get_timestamp():
    return int(time.time() * 1000)

def output_exception(e):
    with open("Error_Message.txt", "a") as error_message:
        error_message.write("Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
        error_message.write(e + "\n\n")

while True:
    # get_position_info() >>>   LONGING  //    SHORTING    // NO_POSITION
    # get_current_trend() >>>  UP_TREND  //   DOWN_TREND   // NO_TRADE_ZONE
    # get_minute_candle() >>> RED_CANDLE //  GREEN_CANDLE  // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

    try:
        trade_action(get_position_info(), get_current_trend(), get_minute_candle())
    except ConnectionResetError as e:
        output_exception(str(e))
        continue
    except BinanceAPIException as e:
        output_exception(str(e))
        continue
    except socket.timeout as e:
        output_exception(str(e))
        continue

    print("Last action executed by " + datetime.now().strftime("%H:%M:%S") + "\n")
    time.sleep(3)
