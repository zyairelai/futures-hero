import os
import time
from binance.client import Client

symbol  =  "BTCUSDT"
bet     =  10

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_my_current_position():
    retrieve_future_position = "Hello"
    if (retrieve_future_position == "I_AM_HOLDING_A_POSITION"):
        return True
    return False

def get_current_trend():
    # The <limit> has to be 3x of the Interval Period
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
        print("🩸 Current Trend is DOWN Trend 🩸")
        trend = "DOWN_TREND"
    elif (current_Open == current_Low):
        print("🥦 Current Trend is UP Trend 🥦")
        trend = "UP_TREND"
    else:
        trend = "NO_TRADE_ZONE"
        if (current_Open > current_Close):
            print("No Trade Zone おやすみ 🩸 ( ͡° ͜ʖ ͡°)")
        elif (current_Close > current_Open):
            print("No Trade Zone おやすみ 🥦 ( ͡° ͜ʖ ͡°)")
        else:
            print("No Color Zone おやすみ ( ͡° ͜ʖ ͡°)")
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
        print("🩸 Current MINUTE is RED 🩸 ")
        minute_candle = "RED_CANDLE"
    elif (current_Open == current_Low):
        print("🥦 Current MINUTE is GREEN 🥦 ")
        minute_candle = "GREEN_CANDLE"
    else:
        if (current_Open > current_Close):
            print("🩸 RED_INDECISIVE おやすみ ( ͡° ͜ʖ ͡°)")
            minute_candle = "RED_INDECISIVE"
        elif (current_Close > current_Open):
            print("🥦 GREEN_INDECISIVE おやすみ ( ͡° ͜ʖ ͡°)")
            minute_candle = "GREEN_INDECISIVE"
        else:
            print("No Trade Zone おやすみ ( ͡° ͜ʖ ͡°)")
            minute_candle = "CLOSE_ALL_POSITION"
    return minute_candle

def get_trade_action(trend, minute_candle):

    if (trend == "UP_TREND") and (minute_candle == "GREEN"):
        print("Action   :   Go Long")
    
    elif (trend == "DOWN_TREND") and (minute_candle == "RED"):
        print("Action   :   Go Short")

    elif trend == "NO_TRADE":
        # Close all position at and quit trading
        print("Action   :   Wait")

    else:
        return "WHATEVER"

while True:
    trend   = get_current_trend()
    minute  = get_minute_candle()

    # get_current_trend() >>> DOWN_TREND // UP_TREND // NO_TRADE_ZONE
    # get_minute_candle() >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // CLOSE_ALL_POSITION

    time.sleep(5)
