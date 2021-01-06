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
    # The <X hour ago UTC> has to be 3x of the Interval Period
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "3 hour ago UTC")

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)

    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        print("🩸 Current Trend is DOWN Trend 🩸 \n")
        return "DOWN_TREND"
    elif (current_Open == current_Low):
        print("🥦 Current Trend is UP Trend 🥦 \n")
        return "UP_TREND"
    else:
        print("No Trade Zone おやすみ ( ͡° ͜ʖ ͡°)\n")
        return "NO_TRADE"

def get_trade_action(HA_Open, HA_Close, HA_High, HA_Low):
    trend = get_current_trend()

    if (current_Open == current_High):
        one_min_candle = "RED"
    elif (current_Open == current_Low):
        one_min_candle = "GREEN"
    else:
        one_min_candle = "INDECISIVE"

    if (trend == "UP_TREND") and (one_min_candle == "GREEN"):
        print("Action   :   Go Long")
    
    elif (trend == "DOWN_TREND") and (one_min_candle == "RED"):
        print("Action   :   Go Short")

    elif trend == "NO_TRADE":
        # Close all position at and quit trading
        print("Action   :   Wait")

    else:
        return "WHATEVER"

previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "3 minute ago UTC")
first_run_Open  = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
first_run_Close = round(((float(previous_klines[0][1]) + float(previous_klines[0][2]) + float(previous_klines[0][3]) + float(previous_klines[0][4])) / 4), 2)
previous_Time   = int(previous_klines[1][0])
previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
previous_Close  = round(((float(previous_klines[1][1]) + float(previous_klines[1][2]) + float(previous_klines[1][3]) + float(previous_klines[1][4])) / 4), 2)

while True:
    current_klines  = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    current_Time    = int(current_klines[0][0])

    if (current_Time - previous_Time) == 60000:
        temp_klines     = current_klines
        current_Open    = round(((previous_Open + previous_Close) / 2), 2)
        current_Close   = round(((float(current_klines[0][1]) + float(current_klines[0][2]) + float(current_klines[0][3]) + float(current_klines[0][4])) / 4), 2)
        current_High    = max(float(current_klines[0][2]), current_Open, current_Close)
        current_Low     = min(float(current_klines[0][3]), current_Open, current_Close)
        
        # trade_action    = get_trade_action(current_Open, current_Close, current_High, current_Low)

        print("[*] Now Sleeping...\n")
        time.sleep(10)
    
    else:
        previous_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "3 minute ago UTC")
        first_run_Open  = round(((float(previous_klines[0][1]) + float(previous_klines[0][4])) / 2), 2)
        first_run_Close = round(((float(previous_klines[0][1]) + float(previous_klines[0][2]) + float(previous_klines[0][3]) + float(previous_klines[0][4])) / 4), 2)
        previous_Time   = int(previous_klines[1][0])
        previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
        previous_Close  = round(((float(previous_klines[1][1]) + float(previous_klines[1][2]) + float(previous_klines[1][3]) + float(previous_klines[1][4])) / 4), 2)
        print("🚀 NEW CANDLE 🚀\n")
