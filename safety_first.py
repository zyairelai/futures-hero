import config
import candlestick
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import war_formation, previous_candle, HEIKIN_ASHI, previous_is_strong

live_trade = config.live_trade
throttle = True # Adding to losing position to pull the entry price

def profit_threshold():
    return 0.2

# ==========================================================================================================================================================================
#     Check on 1HR, 6HR, 12HR, entry on 1 minute, confirmation with candlestick
# ==========================================================================================================================================================================

def lets_make_some_money(i):
    response = binance_futures.position_information(i)[0]
    mark_price   = binance_futures.mark_price(i)
    klines_1min  = binance_futures.KLINE_INTERVAL_1MINUTE(i)
    klines_30MIN = binance_futures.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures.KLINE_INTERVAL_6HOUR(i)
    klines_12HOUR = binance_futures.KLINE_INTERVAL_12HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = profit_threshold()

    heikin_ashi.output_current(mark_price, klines_12HOUR)
    heikin_ashi.output_previous(klines_6HOUR)
    heikin_ashi.output_current(mark_price, klines_6HOUR)
    heikin_ashi.output_current(mark_price, klines_1HOUR)
    heikin_ashi.output_current(mark_price, klines_1min)
    candlestick.output_candle(klines_1min)
    
    if response.get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED(i)
    if int(response.get("leverage")) != config.leverage[i]: binance_futures.change_leverage(i, config.leverage[i])

    if position_info == "LONGING":
        if EXIT_LONG(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")
        elif THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures.throttle(i, "LONG")
            print("ACTION           :   🔥 THROTTLE_LONG 🔥")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        elif THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures.throttle(i, "SHORT")
            print("ACTION           :   🔥 THROTTLE_SHORT 🔥")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if not hot_zone(klines_30MIN, klines_6HOUR) and ALL_CLEAR(mark_price, klines_6HOUR, klines_12HOUR) == "GREEN" and \
            GO_LONG(mark_price, klines_1min, klines_1HOUR):

            if live_trade: binance_futures.open_position(i, "LONG", config.quantity[i])
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif not hot_zone(klines_30MIN, klines_6HOUR) and ALL_CLEAR(mark_price, klines_6HOUR, klines_12HOUR) == "RED" and \
            GO_SHORT(mark_price, klines_1min, klines_1HOUR):

            if live_trade: binance_futures.open_position(i, "SHORT", config.quantity[i])
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

def GO_LONG(mark_price, klines_1min, klines_1HOUR):
        if hybrid_candle(mark_price, klines_1min) == "GREEN" and war_formation(mark_price, klines_1min) and \
            HEIKIN_ASHI(mark_price, klines_1HOUR) == "GREEN" : return True

def GO_SHORT(mark_price, klines_1min, klines_1HOUR):
        if hybrid_candle(mark_price, klines_1min) == "RED" and war_formation(mark_price, klines_1min) and \
            HEIKIN_ASHI(mark_price, klines_1HOUR) == "RED" : return True

def EXIT_LONG(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) > mark_price: return True

def EXIT_SHORT(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) < mark_price: return True

# Adding to the position to pull back the entry price when the maintenance margin is below 70%
throttle_threshold = -0.7

def THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
    if HEIKIN_ASHI(mark_price, klines_6HOUR) != "RED" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 8) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
    if HEIKIN_ASHI(mark_price, klines_6HOUR) != "GREEN" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 8) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

# ==========================================================================================================================================================================
#                                                     TRADE AND NO TRADE ZONE
# ==========================================================================================================================================================================

def clear_direction(mark_price, klines):
    if HEIKIN_ASHI(mark_price, klines) == "GREEN" : current = "GREEN"
    elif HEIKIN_ASHI(mark_price, klines) == "RED" : current = "RED"
    else: current = "INDECISIVE"

    if (previous_candle(klines) == "GREEN" or previous_candle(klines) == "GREEN_INDECISIVE") and previous_is_strong(klines): previous = "GREEN"
    elif (previous_candle(klines) == "RED" or previous_candle(klines) == "RED_INDECISIVE") and previous_is_strong(klines) : previous = "RED"
    else: previous = "INDECISIVE"

    if previous == "GREEN" and current == "GREEN": direction = "GREEN"
    elif previous == "RED" and current == "RED": direction = "RED"
    else: direction = "INDECISIVE"

    return direction

def direction_confirmation(mark_price, klines):
    if HEIKIN_ASHI(mark_price, klines) == "GREEN" : return "GREEN"
    elif HEIKIN_ASHI(mark_price, klines) == "RED" : return "RED"
    else: return "INDECISIVE"

def hybrid_candle(mark_price, klines):
    if HEIKIN_ASHI(mark_price, klines) == "GREEN" and candlestick.CANDLE(klines) == "GREEN" : return "GREEN"
    elif HEIKIN_ASHI(mark_price, klines) == "RED" and candlestick.CANDLE(klines) == "RED" : return "RED"
    else: return "INDECISIVE"

def ALL_CLEAR(mark_price, klines_6HOUR, klines_12HOUR):
    if clear_direction(mark_price, klines_6HOUR) == "GREEN" and \
        direction_confirmation(mark_price, klines_12HOUR) == "GREEN" and \
        hybrid_candle(mark_price, klines_6HOUR) == "GREEN": return "GREEN"
    elif clear_direction(mark_price, klines_6HOUR) == "RED" and \
        direction_confirmation(mark_price, klines_12HOUR) == "RED" and \
        hybrid_candle(mark_price, klines_6HOUR) == "RED": return "RED"

def get_out_zone(klines_30MIN, klines_6HOUR):
    future_direction = binance_futures.timestamp_of(klines_6HOUR) + return_interval(klines_6HOUR)
    get_out_zone = future_direction - return_interval(klines_30MIN)
    if binance_futures.get_timestamp() > get_out_zone: return True

def return_interval(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = 1
    elif milliseconds == 3 * 60000: interval = 3
    elif milliseconds == 5 * 60000: interval = 5
    elif milliseconds == 15 * 60000: interval = 15
    elif milliseconds == 30 * 60000: interval = 30
    elif milliseconds == 1 * 60 * 60000: interval = 1 * 60
    elif milliseconds == 2 * 60 * 60000: interval = 2 * 60
    elif milliseconds == 4 * 60 * 60000: interval = 4 * 60
    elif milliseconds == 6 * 60 * 60000: interval = 6 * 60
    elif milliseconds == 12 * 60 * 60000: interval = 12 * 60
    return (interval * 60000)
