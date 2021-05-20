import config
import candlestick
import get_position
import HA_current, HA_previous
import binance_futures_api
from datetime import datetime
from termcolor import colored

live_trade = config.live_trade
throttle = True # Adding to losing position to pull back the entry price

def profit_threshold():
    return 0.4

# ==========================================================================================================================================================================
#     Check on 6HR and 1HR, the most standard way
# ==========================================================================================================================================================================

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)[0]
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = profit_threshold()

    HA_previous.output(klines_6HOUR)
    HA_current.output(mark_price, klines_6HOUR)
    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_1min)
    
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)
    if int(response.get("leverage")) != config.leverage[i]: binance_futures_api.change_leverage(i, config.leverage[i])

    if position_info == "LONGING":
        if EXIT_LONG(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")

        elif THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures_api.throttle(i, "LONG")
            print("ACTION           :   🔥 THROTTLE_LONG 🔥")

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")

        elif THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
            if live_trade and throttle: binance_futures_api.throttle(i, "SHORT")
            print("ACTION           :   🔥 THROTTLE_SHORT 🔥")

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(mark_price, klines_6HOUR) == "GREEN" and GO_LONG(mark_price, klines_1min, klines_1HOUR):
            if live_trade: binance_futures_api.open_position(i, "LONG", config.quantity[i])
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(mark_price, klines_6HOUR) == "RED" and GO_SHORT(mark_price, klines_1min, klines_1HOUR):
            if live_trade: binance_futures_api.open_position(i, "SHORT", config.quantity[i])
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0] and HA_current.candlebody(klines_6HOUR) > 2 : return True

def clear_direction(mark_price, klines):
    if HA_current.heikin_ashi(mark_price, klines) == "GREEN" : current = "GREEN"
    elif HA_current.heikin_ashi(mark_price, klines) == "RED" : current = "RED"
    else: current = "INDECISIVE"

    if (HA_previous.candle(klines) == "GREEN" or HA_previous.candle(klines) == "GREEN_INDECISIVE") and HA_previous.is_strong(klines): previous = "GREEN"
    elif (HA_previous.candle(klines) == "RED" or HA_previous.candle(klines) == "RED_INDECISIVE") and HA_previous.is_strong(klines) : previous = "RED"
    else: previous = "INDECISIVE"

    if previous == "GREEN" and current == "GREEN": direction = "GREEN"
    elif previous == "RED" and current == "RED": direction = "RED"
    else: direction = "INDECISIVE"

    return direction

def hybrid_candle(mark_price, klines):
    if HA_current.heikin_ashi(mark_price, klines) == "GREEN" and candlestick.CANDLE(klines) == "GREEN" : return "GREEN"
    elif HA_current.heikin_ashi(mark_price, klines) == "RED" and candlestick.CANDLE(klines) == "RED" : return "RED"
    else: return "INDECISIVE"

def GO_LONG(mark_price, klines_1min, klines_1HOUR):
        if hybrid_candle(mark_price, klines_1min) == "GREEN" and HA_current.heikin_ashi(mark_price, klines_1HOUR) != "RED" and \
            HA_current.war_formation(mark_price, klines_1min) : return True

def GO_SHORT(mark_price, klines_1min, klines_1HOUR):
        if hybrid_candle(mark_price, klines_1min) == "RED" and HA_current.heikin_ashi(mark_price, klines_1HOUR) != "GREEN" and \
            HA_current.war_formation(mark_price, klines_1min): return True

def EXIT_LONG(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HA_previous.Close(klines_1min) > mark_price: return True

def EXIT_SHORT(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HA_previous.Close(klines_1min) < mark_price: return True

# Adding to the position to pull back the entry price when the maintenance margin is below 70%
throttle_threshold = -0.7

def THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) != "RED" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 8) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) != "GREEN" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 8) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True
