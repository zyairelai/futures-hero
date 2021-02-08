from pencil_wick import pencil_wick_test

def GO_LONG(one_minute, five_minute):
    if (one_minute == "GREEN") and ((five_minute == "GREEN") or ((five_minute == "GREEN_INDECISIVE") and (pencil_wick_test(5, "GREEN") == "PASS") )) and (pencil_wick_test(1, "GREEN") == "PASS"): return True
    else: return False

def GO_SHORT(one_minute, five_minute):
    if (one_minute == "RED") and ((five_minute == "RED") or ((five_minute == "RED_INDECISIVE") and (pencil_wick_test(5, "GREEN") == "PASS"))) and (pencil_wick_test(1, "RED") == "PASS"): return True
    else: return False

def CLOSE_LONG(five_minute, emergency):
    if (five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick_test(1, "GREEN") == "FAIL"): return True
    else: return False

def CLOSE_SHORT(five_minute, emergency):
    if (five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick_test(1, "RED") == "FAIL"): return True
    else: return False