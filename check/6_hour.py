import os
import time
import config
from binance.client import Client

def get_6hour(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        trend = "DOWN_TREND"
        # print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif (current_Open == current_Low):
        trend = "UP_TREND"
        # print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        # print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

start = time.time()
print("The <6_hour.py> return value is : " + get_6hour())
print(f"Time Taken: {time.time() - start} seconds\n")