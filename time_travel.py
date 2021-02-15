import config
import heikin_ashi
import binance_futures

def check_previous(INTERVAL):
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    if (previous_Open == previous_Low): previous = "GREEN"
    elif (previous_Open == previous_High): previous = "RED"
    elif (previous_Open > previous_Close): previous = "RED_INDECISIVE"
    elif (previous_Close > previous_Open): previous = "GREEN_INDECISIVE"
    else: previous = "NO_MOVEMENT"

    return previous
