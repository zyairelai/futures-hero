import config
import binance_futures
from heikin_ashi import silent_candle

def calculate_trade_amount():
    six_hour = binance_futures.KLINE_INTERVAL_6HOUR(4)

    first_run_Open  = round(((float(six_hour[0][1]) + float(six_hour[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(six_hour[0][1]) + float(six_hour[0][2]) + float(six_hour[0][3]) + float(six_hour[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(six_hour[1][1]) + float(six_hour[1][2]) + float(six_hour[1][3]) + float(six_hour[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(six_hour[2][1]) + float(six_hour[2][2]) + float(six_hour[1][3]) + float(six_hour[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(six_hour[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(six_hour[2][3]), previous_Open, previous_Close)

    if (previous_Open == previous_Low): previous_direction = "GREEN"
    elif (previous_Open == previous_High): previous_direction = "RED"
    else: previous_direction = "INDECISIVE"

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(six_hour[3][1]) + float(six_hour[3][2]) + float(six_hour[3][3]) + float(six_hour[3][4])) / 4), config.round_decimal)
    current_High    = max(float(six_hour[3][2]), current_Open, current_Close)
    current_Low     = min(float(six_hour[3][3]), current_Open, current_Close)

    if (current_Open == current_Low): current_direction = "GREEN"
    elif (current_Open == current_High): current_direction = "RED"
    else: current_direction = "INDECISIVE"

    markPrice = float(binance_futures.position_information()[0].get("markPrice"))

    if previous_direction == "INDECISIVE" or current_direction == "INDECISIVE": trade_amount = config.quantity * 1   # Dangerous Witching Hour // Minimum Trade Amount

    elif (previous_direction != "INDECISIVE") and (current_direction == "GREEN"):
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
