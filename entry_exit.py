import config
import binance_futures
from pencil_wick import re_entry
from pencil_wick import pencil_wick_test

def GO_LONG(one_minute, five_minute):
    if ((one_minute == "GREEN") and (pencil_wick_test("GREEN") == "PASS")) and ((five_minute == "GREEN") and (re_entry("GREEN") == "PASS")): return True
    # if ((one_minute == "GREEN") and (pencil_wick_test("GREEN") == "PASS")) and (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (re_entry("GREEN") == "PASS")): return True
    else: return False

def GO_SHORT(one_minute, five_minute):
    if ((one_minute == "RED") and (pencil_wick_test("RED") == "PASS")) and ((five_minute == "RED") and (re_entry("RED") == "PASS")): return True
    # if ((one_minute == "RED") and (pencil_wick_test("RED") == "PASS")) and (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (re_entry("RED") == "PASS")): return True
    else: return False

def CLOSE_LONG(exit_minute):
    if (exit_minute == "RED") or (pencil_wick_test("GREEN") == "FAIL"): return True
    else: return False

def CLOSE_SHORT(exit_minute):
    if (exit_minute == "GREEN") or (pencil_wick_test("RED") == "FAIL"): return True
    else: return False

def EMERGENCY_EXIT_LONG(five_minute):
    if ((five_minute == "RED") and (re_entry("RED") == "PASS")): return True
    # if (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (re_entry("RED") == "PASS")): return True
    else: return False

def EMERGENCY_EXIT_SHORT(five_minute):
    if ((five_minute == "GREEN") and (re_entry("GREEN") == "PASS")): return True
    # if (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (re_entry("GREEN") == "PASS")): return True
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
    elif (previous_Open > previous_Close): previous_candle = "RED_INDECISIVE"
    elif (previous_Close > previous_Open): previous_candle = "GREEN_INDECISIVE"
    else: previous_candle = "NO_MOVEMENT"

    if EXIT == "SHORT":
        if ((previous_candle == "GREEN") or (previous_candle == "GREEN_INDECISIVE")) and (current_High > previous_High): return True
        else: return False
    elif EXIT == "LONG":
        if ((previous_candle == "RED") or (previous_candle == "RED_INDECISIVE")) and(current_Low < previous_Low): return True
        else: return False
