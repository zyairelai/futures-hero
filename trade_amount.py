import config
import heikin_ashi
import binance_futures

def calculate_trade_amount():
    # klines       = binance_futures.KLINE_INTERVAL_6HOUR()
    # first_six    = heikin_ashi.first_candle(klines)
    # previous_six = heikin_ashi.previous_candle(klines)
    # current_six  = heikin_ashi.current_candle(klines)
    
    # if   (first_six != "GREEN") and (previous_six == "GREEN") and (current_six == "GREEN")  : six_hour = "SAFE"
    # elif (first_six != "RED")   and (previous_six == "RED")   and (current_six == "RED")    : six_hour = "SAFE"
    # else: six_hour = "NOT_SURE"

    firstrun_volume = binance_futures.get_volume("FIRSTRUN", "6HOUR")
    previous_volume = binance_futures.get_volume("PREVIOUS", "6HOUR")
    current_volume  = binance_futures.get_volume("CURRENT", "6HOUR")

    if (firstrun_volume > previous_volume) and (previous_volume > current_volume): mode = "DANGER"
    elif (current_volume > previous_volume) and (previous_volume > firstrun_volume): mode = "SAFE"
    else: mode = "MODERATE"

    if   mode == "SAFE"     : trade_amount = config.quantity * 3
    elif mode == "MODERATE" : trade_amount = config.quantity * 2
    else: trade_amount = config.quantity * 1
    return trade_amount

def old_trade_amount():
    six_hour = binance_futures.KLINE_INTERVAL_6HOUR()

    if   (heikin_ashi.previous_Open(six_hour) == heikin_ashi.previous_Low(six_hour)) : previous_direction = "GREEN"
    elif (heikin_ashi.previous_Open(six_hour) == heikin_ashi.previous_High(six_hour)): previous_direction = "RED"
    else: previous_direction = "INDECISIVE"

    if   (heikin_ashi.current_Open(six_hour) == heikin_ashi.current_Low(six_hour)) : current_direction = "GREEN"
    elif (heikin_ashi.current_Open(six_hour) == heikin_ashi.current_High(six_hour)): current_direction = "RED"
    else: current_direction = "INDECISIVE"

    markPrice = float(binance_futures.position_information()[0].get("markPrice"))

    if (previous_direction != "INDECISIVE") and (current_direction == "GREEN"):
        if heikin_ashi.current_High(six_hour) > heikin_ashi.previous_High(six_hour):
            if   (markPrice < heikin_ashi.previous_High(six_hour)) or (markPrice < heikin_ashi.current_Close(six_hour)): trade_amount = config.quantity * 3     # Maximum Trade Amount
            elif (markPrice > heikin_ashi.previous_High(six_hour)) or (markPrice > heikin_ashi.current_Close(six_hour)): trade_amount = config.quantity * 1     # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice > heikin_ashi.current_Close(six_hour): trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1    # Minimum Trade Amount

    elif (previous_direction != "INDECISIVE") and (current_direction == "RED"):
        if heikin_ashi.current_Low(six_hour) < heikin_ashi.previous_Low(six_hour):
            if   (markPrice > heikin_ashi.previous_Low(six_hour)) or (markPrice > heikin_ashi.current_Close(six_hour)): trade_amount = config.quantity * 3      # Maximum Trade Amount
            elif (markPrice < heikin_ashi.previous_Low(six_hour)) or (markPrice < heikin_ashi.current_Close(six_hour)): trade_amount = config.quantity * 1      # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice < heikin_ashi.current_Close(six_hour): trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1                            # Minimum Trade Amount

    else: trade_amount = config.quantity * 1
    return trade_amount
