import config
import heikin_ashi
import binance_futures

def calculate_trade_amount():
    klines       = binance_futures.KLINE_INTERVAL_6HOUR()
    first_six    = heikin_ashi.first_candle(klines)
    previous_six = heikin_ashi.previous_candle(klines)
    current_six  = heikin_ashi.current_candle(klines)
    
    if   (first_six != "GREEN") and (previous_six == "GREEN") and (current_six == "GREEN")  : six_hour = "SAFE"
    elif (first_six != "RED")   and (previous_six == "RED")   and (current_six == "RED")    : six_hour = "SAFE"
    else: six_hour = "NOT_SURE"

    klines       = binance_futures.KLINE_INTERVAL_1HOUR()
    first_one    = heikin_ashi.first_candle(klines)
    previous_one = heikin_ashi.previous_candle(klines)
    current_one  = heikin_ashi.current_candle(klines)

    if   (first_one != "GREEN") and (previous_one == "GREEN") and (current_one == "GREEN")  : one_hour = "SAFE"
    elif (first_one != "RED")   and (previous_one == "RED")   and (current_one == "RED")    : one_hour = "SAFE"
    else: one_hour = "NOT_SURE"

    if   six_hour == "SAFE" and one_hour == "SAFE"     : mode = "SAFE"
    elif six_hour == "SAFE" and one_hour == "NOT_SURE" : mode = "MODERATE"
    else: mode = "NOT_SURE"

    if   mode == "SAFE"     : trade_amount = config.quantity * 3
    elif mode == "MODERATE" : trade_amount = config.quantity * 2
    else: trade_amount = config.quantity * 1
    return trade_amount

def initial_Open(klines)  : return round(((float(klines[-4][1]) + float(klines[-4][4])) / 2), config.round_decimal)
def initial_Close(klines) : return round(((float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4), config.round_decimal)

def first_Open(klines)    : return round(((initial_Open(klines) + initial_Close(klines)) / 2), config.round_decimal)
def first_Close(klines)   : return round(((float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4), config.round_decimal)
def first_High(klines)    : return max(float(klines[-3][2]), first_Open(klines), first_Close(klines))
def first_Low(klines)     : return min(float(klines[-3][3]), first_Open(klines), first_Close(klines))

def previous_Open(klines) : return round(((first_Open(klines) + first_Close(klines)) / 2), config.round_decimal)
def previous_Close(klines): return round(((float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4), config.round_decimal)
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines)  : return round(((previous_Open(klines) + previous_Close(klines)) / 2), config.round_decimal)
def current_Close(klines) : return round(((float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4), config.round_decimal)
def current_High(klines)  : return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines)   : return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

def old_trade_amount():
    six_hour = binance_futures.KLINE_INTERVAL_6HOUR()

    if   (previous_Open(six_hour) == previous_Low(six_hour)) : previous_direction = "GREEN"
    elif (previous_Open(six_hour) == previous_High(six_hour)): previous_direction = "RED"
    else: previous_direction = "INDECISIVE"

    if   (current_Open(six_hour) == current_Low(six_hour)) : current_direction = "GREEN"
    elif (current_Open(six_hour) == current_High(six_hour)): current_direction = "RED"
    else: current_direction = "INDECISIVE"

    markPrice = float(binance_futures.position_information()[0].get("markPrice"))

    if (previous_direction != "INDECISIVE") and (current_direction == "GREEN"):
        if current_High(six_hour) > previous_High(six_hour):
            if   (markPrice < previous_High(six_hour)) or (markPrice < current_Close(six_hour)): trade_amount = config.quantity * 3     # Maximum Trade Amount
            elif (markPrice > previous_High(six_hour)) or (markPrice > current_Close(six_hour)): trade_amount = config.quantity * 1     # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice > current_Close(six_hour): trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1    # Minimum Trade Amount

    elif (previous_direction != "INDECISIVE") and (current_direction == "RED"):
        if current_Low(six_hour) < previous_Low(six_hour):
            if   (markPrice > previous_Low(six_hour)) or (markPrice > current_Close(six_hour)): trade_amount = config.quantity * 3      # Maximum Trade Amount
            elif (markPrice < previous_Low(six_hour)) or (markPrice < current_Close(six_hour)): trade_amount = config.quantity * 1      # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice < current_Close(six_hour): trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1                            # Minimum Trade Amount

    else: trade_amount = config.quantity * 1
    return trade_amount
