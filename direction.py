import HA_current, HA_previous

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

def current_direction(mark_price, klines):
    # If candle_size is less than 2%, the candle is too small to trade
    DO_NOT_FOMO = HA_current.candle_size(klines) > 2
    if HA_current.heikin_ashi(mark_price, klines) == "GREEN" and DO_NOT_FOMO: return "GREEN"
    elif HA_current.heikin_ashi(mark_price, klines) == "RED" and DO_NOT_FOMO: return "RED"
    else: return "INDECISIVE"

def clear_direction(mark_price, klines):
    if (HA_previous.candle(klines) == "GREEN" or HA_previous.candle(klines) == "GREEN_INDECISIVE") and HA_previous.is_strong(klines): previous = "GREEN"
    elif (HA_previous.candle(klines) == "RED" or HA_previous.candle(klines) == "RED_INDECISIVE") and HA_previous.is_strong(klines) : previous = "RED"
    else: previous = "INDECISIVE"

    if previous == "GREEN" and current_direction(mark_price, klines) == "GREEN": direction = "GREEN"
    elif previous == "RED" and current_direction(mark_price, klines) == "RED": direction = "RED"
    else: direction = "INDECISIVE"

    return direction
