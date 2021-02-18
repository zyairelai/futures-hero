import config
import binance_futures
from pencil_wick import one_minute_entry_test
from pencil_wick import one_minute_exit_test
from pencil_wick import five_minute_test
from pencil_wick import one_hour_test
from time_travel import check_previous

def GO_LONG(one_minute, five_minute, one_hour):
    if ((one_minute == "GREEN") and (one_minute_entry_test("GREEN") == "PASS")) and \
       (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (five_minute_test("GREEN") == "PASS")) and \
       ((one_hour != "RED" or one_hour != "RED_INDECISIVE") and (one_hour_test("RED") == "FAIL")): return True
    else: return False

def GO_SHORT(one_minute, five_minute, one_hour):
    if ((one_minute == "RED") and (one_minute_entry_test("RED") == "PASS")) and \
       (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (five_minute_test("RED") == "PASS")) and \
       (((one_hour != "GREEN") or (one_hour != "GREEN_INDECISIVE")) and (one_hour_test("GREEN") == "FAIL")): return True
    else: return False

def CLOSE_LONG(exit_minute):
    if (exit_minute == "RED") or (one_minute_exit_test("GREEN") == "PASS"): return True
    else: return False

def CLOSE_SHORT(exit_minute):
    if (exit_minute == "GREEN") or (one_minute_exit_test("RED") == "PASS"): return True
    else: return False

def DIRECTION_CHANGE_EXIT_LONG(one_hour, six_hour):
    if ((one_hour == "RED") and (one_hour_test("RED") == "PASS")) or \
       ((one_hour == "RED_INDECISIVE") and (check_previous("1HOUR") == "GREEN")) and (one_hour_test("RED") == "PASS") or \
       ((six_hour == "RED") and ((one_hour == "RED") or (one_hour == "RED_INDECISIVE")) and one_hour_test("RED") == "PASS"): return True
    else: return False

def DIRECTION_CHANGE_EXIT_SHORT(one_hour, six_hour):
    if ((one_hour == "GREEN") and (one_hour_test("GREEN") == "PASS")) or \
       ((one_hour == "GREEN_INDECISIVE") and (check_previous("1HOUR") == "RED") and (one_hour_test("GREEN") == "PASS")) or \
       ((six_hour == "GREEN") and ((one_hour == "GREEN") or (one_hour == "GREEN_INDECISIVE")) and one_hour_test("GREEN") == "PASS"): return True
    else: return False
