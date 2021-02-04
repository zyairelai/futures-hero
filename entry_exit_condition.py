from pencil_wick import pencil_wick_test

def ENTER_LONG(one_minute, five_minute):
    if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (pencil_wick_test("GREEN") == "PASS"): return True
    else: return False

def ENTER_SHORT(one_minute, five_minute):
    if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (pencil_wick_test("RED") == "PASS"): return True
    else: return False

def EXIT_LONG(five_minute, emergency):
    if (five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick_test("GREEN") == "FAIL"): return True
    else: return False

def EXIT_SHORT(five_minute, emergency):
    if (five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick_test("RED") == "FAIL"): return True
    else: return False