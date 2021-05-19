import config
import candlestick
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import HEIKIN_ASHI

live_trade = config.live_trade

def profit_threshold():
    return 0.4

# ==========================================================================================================================================================================
#     Check on 1HR and 15MIN lower leverage play, NO THROTTLE
# ==========================================================================================================================================================================

def lets_make_some_money(i):
    response = binance_futures.position_information(i)[0]
    mark_price   = binance_futures.mark_price(i)
    klines_15min = binance_futures.KLINE_INTERVAL_15MINUTE(i)
    klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR(i)
    position_info = get_position.get_position_info(i, response)
    using_lower_leverage = config.leverage[i]
    profit = profit_threshold()

    heikin_ashi.output_current(mark_price, klines_1HOUR)
    heikin_ashi.output_current(mark_price, klines_15min)

    if response.get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED(i)
    if int(response.get("leverage")) != using_lower_leverage: binance_futures.change_leverage(i, using_lower_leverage)

    if position_info == "LONGING":
        if EXIT_LONG(response, mark_price, profit, klines_15min, klines_1HOUR):
            if live_trade: binance_futures.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(response, mark_price, profit, klines_15min, klines_1HOUR):
            if live_trade: binance_futures.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if HEIKIN_ASHI(mark_price, klines_1HOUR) == "GREEN" and HEIKIN_ASHI(mark_price, klines_15min):
            if live_trade: binance_futures.open_position(i, "LONG", config.quantity[i])
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif HEIKIN_ASHI(mark_price, klines_1HOUR) == "RED" and HEIKIN_ASHI(mark_price, klines_15min):
            if live_trade: binance_futures.open_position(i, "SHORT", config.quantity[i])
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

def hybrid_candle(mark_price, klines):
    if HEIKIN_ASHI(mark_price, klines) == "GREEN" and candlestick.CANDLE(klines) == "GREEN" : return "GREEN"
    elif HEIKIN_ASHI(mark_price, klines) == "RED" and candlestick.CANDLE(klines) == "RED" : return "RED"
    else: return "INDECISIVE"

def GO_LONG(mark_price, klines_15min):
        if hybrid_candle(mark_price, klines_15min) == "GREEN": return True

def GO_SHORT(mark_price, klines_15min):
        if hybrid_candle(mark_price, klines_15min) == "RED": return True

def EXIT_LONG(response, mark_price, profit, klines_15min, klines_1HOUR):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HEIKIN_ASHI(mark_price, klines_15min) == "RED" : return True
    else:
        if HEIKIN_ASHI(mark_price, klines_1HOUR) == "RED": return True

def EXIT_SHORT(response, mark_price, profit, klines_15min, klines_1HOUR):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HEIKIN_ASHI(mark_price, klines_15min) == "GREEN": return True
    else:
        if HEIKIN_ASHI(mark_price, klines_1HOUR) == "GREEN": return True
