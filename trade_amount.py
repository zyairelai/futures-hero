import config
import binance_futures
from heikin_ashi import silent_candle

def initial_O(klines): return round(((float(klines[-4][1]) + float(klines[-4][4])) / 2), config.round_decimal)
def initial_C(klines): return round(((float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4), config.round_decimal)

def first_O(klines): return round(((initial_O(klines) + initial_C(klines)) / 2), config.round_decimal)
def first_C(klines): return round(((float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4), config.round_decimal)
def first_H(klines): return max(float(klines[-3][2]), first_O(klines), first_C(klines))
def first_L(klines): return min(float(klines[-3][3]), first_O(klines), first_C(klines))

def previous_O(klines): return round(((first_O(klines) + first_C(klines)) / 2), config.round_decimal)
def previous_C(klines): return round(((float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4), config.round_decimal)
def previous_H(klines): return max(float(klines[-2][2]), previous_O(klines), previous_C(klines))
def previous_L(klines): return min(float(klines[-2][3]), previous_O(klines), previous_C(klines))

def current_O(klines): return round(((previous_O(klines) + previous_C(klines)) / 2), config.round_decimal)
def current_C(klines): return round(((float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4), config.round_decimal)
def current_H(klines): return max(float(klines[-1][2]), current_O(klines), current_C(klines))
def current_L(klines): return min(float(klines[-1][3]), current_O(klines), current_C(klines))

def calculate_trade_amount():
    six_hour = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if (previous_Open == previous_Low): previous_direction = "GREEN"
    elif (previous_Open == previous_High): previous_direction = "RED"
    else: previous_direction = "INDECISIVE"

    if (current_Open == current_Low): current_direction = "GREEN"
    elif (current_Open == current_High): current_direction = "RED"
    else: current_direction = "INDECISIVE"

    markPrice = float(binance_futures.position_information()[0].get("markPrice"))

    if (previous_direction != "INDECISIVE") and (current_direction == "GREEN"):
        if current_High > previous_High:
            if (markPrice < previous_High) or (markPrice < current_Close): trade_amount = config.quantity * 3       # Maximum Trade Amount
            elif (markPrice > previous_High) or (markPrice > current_Close): trade_amount = config.quantity * 1     # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice > current_Close: trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1    # Minimum Trade Amount

    elif (previous_direction != "INDECISIVE") and (current_direction == "RED"):
        if current_Low < previous_Low:
            if (markPrice > previous_Low) or (markPrice > current_Close): trade_amount = config.quantity * 3        # Maximum Trade Amount
            elif (markPrice < previous_Low) or (markPrice < current_Close): trade_amount = config.quantity * 1      # Minimum Trade Amount
            else: trade_amount = config.quantity * 2    # Moderate Trade Amount
        else:
            if markPrice < current_Close: trade_amount = config.quantity * 2    # Moderate Trade Amount
            else: trade_amount = config.quantity * 1                            # Minimum Trade Amount

    return trade_amount
