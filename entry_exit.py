from pencil_wick import re_entry
from pencil_wick import pencil_wick_test

def GO_LONG(one_minute, five_minute):
    if ((one_minute == "GREEN") and (pencil_wick_test("GREEN") == "PASS")) and (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (re_entry("GREEN") == "PASS")): return True
    else: return False

def GO_SHORT(one_minute, five_minute):
    if ((one_minute == "RED") and (pencil_wick_test("RED") == "PASS")) and (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (re_entry("RED") == "PASS")): return True
    else: return False

def CLOSE_LONG(exit_minute):
    if (exit_minute == "RED") or (pencil_wick_test("GREEN") == "FAIL"): return True
    else: return False

def CLOSE_SHORT(exit_minute):
    if (exit_minute == "GREEN") or (pencil_wick_test("RED") == "FAIL"): return True
    else: return False

def EMERGENCY_EXIT_LONG(five_minute):
    if ((five_minute == "RED") and (re_entry("RED") == "PASS")): return True
    else: return False

def EMERGENCY_EXIT_SHORT(five_minute):
    if ((five_minute == "GREEN") and (re_entry("GREEN") == "PASS")): return True
    else: return False