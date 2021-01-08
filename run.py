import api
import time
from datetime import datetime
from binance.client import Client

symbol  =  "BTCUSDT"
bet     =  10

# Get environment variables
api_key     = api.get_key()
api_secret  = api.get_secret()
client      = Client(api_key, api_secret)

def get_my_current_position():
    retrieve_future_position = "Hello"
    if (retrieve_future_position == "I_AM_HOLDING_A_POSITION"):
        return True
    return False

def get_current_trend():
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        print("Current TREND    :   🩸 DOWN Trend 🩸")
        trend = "DOWN_TREND"
    elif (current_Open == current_Low):
        print("Current TREND    :   🥦 UP Trend 🥦")
        trend = "UP_TREND"
    else:
        trend = "NO_TRADE_ZONE"
        if (current_Open > current_Close):
            print("Current TREND    :   😴 No Trade Zone おやすみ 🩸")
        elif (current_Close > current_Open):
            print("Current TREND    :   😴 No Trade Zone おやすみ 🥦")
        else:
            print("Current TREND    :   😴 No Color Zone おやすみ ( ͡° ͜ʖ ͡°)")
    return trend

def get_minute_candle():
    # The <limit> has to be 3x of the Interval Period
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        print("Current MINUTE   :   🩸 RED 🩸")
        minute_candle = "RED_CANDLE"
    elif (current_Open == current_Low):
        print("Current MINUTE   :   🥦 GREEN 🥦")
        minute_candle = "GREEN_CANDLE"
    else:
        if (current_Open > current_Close):
            print("Current MINUTE   :   RED_INDECISIVE 🩸")
            minute_candle = "RED_INDECISIVE"
        elif (current_Close > current_Open):
            print("Current MINUTE   :   GREEN_INDECISIVE 🥦")
            minute_candle = "GREEN_INDECISIVE"
        else:
            print("❗Something in get_minute_candle() is going wrong❗")
            minute_candle = "CLOSE_ALL_POSITION"
    return minute_candle

def get_trade_action(trend, minute_candle):
    if trend == "NO_TRADE_ZONE":
        # Close all position at and quit trading
        print("Action           :   Close Everything and Wait 🦄")
        trade_action = "CLOSE_ALL_POSITION"
    elif (trend == "UP_TREND"):
        if (minute_candle == "GREEN_CANDLE"):
            print("Action           :   GO_LONG 🚀")
            trade_action = "GO_LONG"
        elif (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   WAIT 🐺")
            trade_action = "WAIT"
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   CLOSE_LONG 😋 && WAIT 🐺")
            trade_action = "CLOSE_LONG"
    elif (trend == "DOWN_TREND"):
        if (minute_candle == "RED_CANDLE"):
            print("Action           :   GO_SHORT 💥")
            trade_action = "GO_SHORT"
        elif (minute_candle == "RED_INDECISIVE"):
            print("Action           :   WAIT 🐺")
            trade_action = "WAIT"
        elif (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   CLOSE_SHORT 😋 && WAIT 🐺")
            trade_action = "CLOSE_SHORT"
    else:
        print("❗Something in get_trade_action() is going wrong❗")
        trade_action = "CLOSE_ALL_POSITION"

    return trade_action

while True:
    # get_current_trend() >>> DOWN_TREND // UP_TREND // NO_TRADE_ZONE
    # get_minute_candle() >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // CLOSE_ALL_POSITION

    trend   = get_current_trend()
    minute  = get_minute_candle()
    action  = get_trade_action(trend, minute)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Last action executed by " + current_time + "\n")

    time.sleep(5)
