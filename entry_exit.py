import config
import binance_futures
from pencil_wick import one_minute_test
from pencil_wick import five_minute_test
from pencil_wick import one_hour_test

def GO_LONG(one_minute, five_minute):
    # if ((one_minute == "GREEN") and (one_minute_test("GREEN") == "PASS")) and ((five_minute == "GREEN") and (five_minute_test("GREEN") == "PASS")): return True # Too Slow
    if ((one_minute == "GREEN") and (one_minute_test("GREEN") == "PASS")) and (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (five_minute_test("GREEN") == "PASS")): return True
    else: return False

def GO_SHORT(one_minute, five_minute):
    # if ((one_minute == "RED") and (one_minute_test("RED") == "PASS")) and ((five_minute == "RED") and (five_minute_test("RED") == "PASS")): return True # Too Slow
    if ((one_minute == "RED") and (one_minute_test("RED") == "PASS")) and (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (five_minute_test("RED") == "PASS")): return True
    else: return False

def CLOSE_LONG(exit_minute):
    if (exit_minute == "RED") or (one_minute_test("GREEN") == "FAIL"): return True
    else: return False

def CLOSE_SHORT(exit_minute):
    if (exit_minute == "GREEN") or (one_minute_test("RED") == "FAIL"): return True
    else: return False

def EMERGENCY_EXIT(EXIT):
    klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if (previous_Open == previous_High): previous_candle = "RED"
    elif (previous_Open == previous_Low): previous_candle = "GREEN"
    # elif (previous_Open > previous_Close): previous_candle = "RED_INDECISIVE"
    # elif (previous_Close > previous_Open): previous_candle = "GREEN_INDECISIVE"
    else: previous_candle = "INDECISIVE"

    if EXIT == "SHORT":
        if ((previous_candle == "INDECISIVE") or (previous_candle == "GREEN")) and (current_High > previous_High): return True
        else: return False
    elif EXIT == "LONG":
        if ((previous_candle == "INDECISIVE") or (previous_candle == "RED")) and(current_Low < previous_Low): return True
        else: return False

def DIRECTION_CHANGE_EXIT_LONG(one_hour):
    if ((one_hour == "RED") and (one_hour_test("RED") == "PASS")): return True
    # if (((one_hour == "RED") or (one_hour == "INDECISIVE")) and (one_hour_test("RED") == "PASS")): return True
    else: return False

def DIRECTION_CHANGE_EXIT_SHORT(one_hour):
    if ((one_hour == "GREEN") and (one_hour_test("GREEN") == "PASS")): return True
    # if (((one_hour == "GREEN") or (one_hour == "INDECISIVE")) and (one_hour_test("GREEN") == "PASS")): return True
    else: return False