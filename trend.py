import os
import time
from binance.client import Client

symbol  =  "BTCUSDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_current_trend():
    # The <X hour ago UTC> has to be 3x of the Interval Period
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "3 hour ago UTC")

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)

    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Time    = int(klines[2][0])
    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    print("The current_Time is  :   " + str(current_Time))
    print("The current_Open is  :   " + str(current_Open))
    print("The current_Close is :   " + str(current_Close))
    print("The current_High is  :   " + str(current_High))
    print("The current_Low is   :   " + str(current_Low) + "")

    if (current_Open == current_High):
        print("📉 Down Trend        :   SHORT\n")
        return "SHORT"
    elif (current_Open == current_Low):
        print("📈 Up Trend          :   LONG\n")
        return "LONG"
    else:
        print("( v￣▽￣) おやすみ ( ͡° ͜ʖ ͡°)\n")
        return "WAIT"
