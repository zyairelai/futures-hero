import config
import binance_futures
from heikin_ashi import silent_candle
from heikin_ashi import entry_test
from heikin_ashi import one_minute_exit_test
from heikin_ashi import check_previous
from heikin_ashi import pattern_broken

def GO_LONG(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "GREEN") and (entry_test("GREEN", "1MINUTE") == "PASS")) and \
       (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (entry_test("GREEN", "5MINUTE") == "PASS")) and \
       ((one_hour != "RED" or one_hour != "RED_INDECISIVE") and (entry_test("RED", "1HOUR") == "FAIL")): return True

def GO_SHORT(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "RED") and (entry_test("RED", "1MINUTE") == "PASS")) and \
       (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (entry_test("RED", "5MINUTE") == "PASS")) and \
       (((one_hour != "GREEN") or (one_hour != "GREEN_INDECISIVE")) and (entry_test("GREEN", "1HOUR") == "FAIL")): return True

def CLOSE_LONG():
    if (one_minute_exit_test("GREEN") == "PASS"): return True

def CLOSE_SHORT():
    if (one_minute_exit_test("RED") == "PASS"): return True

def DIRECTION_CHANGE_EXIT_LONG(one_hour):
    if ((one_hour == "RED") and (entry_test("RED", "1MINUTE") == "PASS")) or \
       ((silent_candle("30MINUTE") == "RED") and (entry_test("RED", "30MINUTE") == "PASS")) or \
       ((one_hour == "RED_INDECISIVE") and (check_previous("1HOUR") == "GREEN")) and (entry_test("RED", "1MINUTE") == "PASS"): return True

def DIRECTION_CHANGE_EXIT_SHORT(one_hour):
    if ((one_hour == "GREEN") and (entry_test("GREEN", "1MINUTE") == "PASS")) or \
       ((silent_candle("30MINUTE") == "GREEN") and (entry_test("GREEN", "30MINUTE") == "PASS")) or \
       ((one_hour == "GREEN_INDECISIVE") and (check_previous("1HOUR") == "RED") and (entry_test("GREEN", "1MINUTE") == "PASS")): return True
