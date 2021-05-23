import binance_futures_api
import config, get_position
import direction, place_order
import HA_current, HA_previous
from datetime import datetime
from termcolor import colored

live_trade = config.live_trade

# ==========================================================================================================================================================================
#     FOMO STRATEGY : Check on 1HR, entry on 1 minute, with 5 minute and 15 minute confirmation to avoid Fake Out
# ==========================================================================================================================================================================

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)[0]
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_5min  = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
    klines_15min = binance_futures_api.KLINE_INTERVAL_15MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = 0.4

    HA_current.output(mark_price, klines_6HOUR)
    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_1min)
    
    leverage = int(config.leverage[i] + 10)
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if place_order.EXIT_LONG(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if place_order.EXIT_SHORT(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            direction.current_direction(mark_price, klines_6HOUR) != "INDECISIVE" and \
            place_order.GO_LONG_ADVANCED(mark_price, klines_1min, klines_5min, klines_15min, klines_1HOUR):

            if live_trade: binance_futures_api.open_position(i, "LONG", config.quantity[i])
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            direction.current_direction(mark_price, klines_6HOUR) != "INDECISIVE" and \
            place_order.GO_SHORT_ADVANCED(mark_price, klines_1min, klines_5min, klines_15min, klines_1HOUR):

            if live_trade: binance_futures_api.open_position(i, "SHORT", config.quantity[i])
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
