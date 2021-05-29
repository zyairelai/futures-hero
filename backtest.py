import os, config, HA_previous
from datetime import datetime
from termcolor import colored

# ==========================================================================================================================================================================
#                                           EXIT CONDITION simulation
# ==========================================================================================================================================================================

def trigger_backtest(i, mark_price, profit, klines_1min):
    if not os.path.exists(os.path.join("BACKTEST", config.pair[i])): os.makedirs(os.path.join("BACKTEST", config.pair[i]))
    imaginary_position = retrieve_position(i)
    unRealizedProfit = unrealizedPnL(i, mark_price)
    if imaginary_position == "LONGING":
        if demo_exit_long(i, mark_price, profit, klines_1min):
            append_close_position(i)
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else:
            print(colored("ACTION           :   HOLDING_LONG", "green"))
            if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
            else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

    elif imaginary_position == "SHORTING":
        if demo_exit_short(i, mark_price, profit, klines_1min):
            append_close_position(i)
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else:
            print(colored("ACTION           :   HOLDING_SHORT", "red"))
            if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
            else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

# ==========================================================================================================================================================================
#                                           LONG and SHORT simulation
# ==========================================================================================================================================================================

def demo_long(i, mark_price):
    if retrieve_position(i) == "NONE":
        record_price(i, mark_price)
        append_open_position(i, "LONG ")
        with open((os.path.join("BACKTEST", config.pair[i], "position.txt")), "w", encoding="utf-8") as message:
            message.write("LONGING")
        print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

def demo_short(i, mark_price):
    if retrieve_position(i) == "NONE":
        record_price(i, mark_price)
        append_open_position(i, "SHORT")
        with open((os.path.join("BACKTEST", config.pair[i], "position.txt")), "w", encoding="utf-8") as message:
            message.write("SHORTING")
        print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

def demo_exit_long(i, mark_price, profit, klines_1min):
    leverage = config.leverage[i]
    current_percentage = unrealizedPnL(i, mark_price)
    if current_percentage > profit:
        if HA_previous.close(klines_1min) > mark_price:
            realized_Pnl = round((current_percentage - 0.2) * leverage , 2)
            append_PnL(i, realized_Pnl)
            reset_position(i)
            return True

    elif current_percentage <= liquidation_threshold(i):
        append_PnL(i, -100)
        append_close_position(i)
        reset_position(i)
        return True

def demo_exit_short(i, mark_price, profit, klines_1min):
    leverage = config.leverage[i]
    current_percentage = unrealizedPnL(i, mark_price)
    if current_percentage > profit:
        if HA_previous.close(klines_1min) < mark_price:
            realized_Pnl = round((current_percentage - 0.2) * leverage , 2)
            append_PnL(i, realized_Pnl)
            reset_position(i)
            return True

    elif current_percentage <= liquidation_threshold(i):
        append_PnL(i, -100)
        append_close_position(i)
        reset_position(i)
        return True

def liquidation_threshold(i):
    return -round((80 / config.leverage[i]), 2)

# ==========================================================================================================================================================================
#                                           System Temporarily Record
# ==========================================================================================================================================================================

def append_PnL(i, realized_PnL):
    with open((os.path.join("BACKTEST", config.pair[i], "PNL.txt")), "a", encoding="utf-8") as message:
        message.write(str(realized_PnL))
        message.write("\n")
    with open((os.path.join("BACKTEST", config.pair[i], "position.txt")), "w", encoding="utf-8") as message:
        message.write("NONE")

def append_open_position(i, position):
    with open((os.path.join("BACKTEST", config.pair[i], "timestamp.txt")), "a", encoding="utf-8") as message:
        message.write(position + " - Last action executed @ " + datetime.now().strftime("%H:%M:%S\n"))

def append_close_position(i):
    with open((os.path.join("BACKTEST", config.pair[i], "timestamp.txt")), "a", encoding="utf-8") as message:
        message.write("CLOSE - Last action executed @ " + datetime.now().strftime("%H:%M:%S\n\n"))

def record_price(i, mark_price):
    with open((os.path.join("BACKTEST", config.pair[i], "price.txt")), "w", encoding="utf-8") as message:
        message.write(str(mark_price))

def retrieve_price(i):
    with open((os.path.join("BACKTEST", config.pair[i], "price.txt")), "r", encoding="utf-8") as message:
        return float(message.readlines()[0])

def retrieve_position(i):
    if not os.path.isfile(os.path.join("BACKTEST", config.pair[i], "position.txt")): reset_position(i)
    with open((os.path.join("BACKTEST", config.pair[i], "position.txt")), "r", encoding="utf-8") as message:
        return str(message.readlines()[0])

def reset_position(i):
    with open((os.path.join("BACKTEST", config.pair[i], "position.txt")), "w", encoding="utf-8") as message:
        message.write("NONE")

def unrealizedPnL(i, mark_price):
    price_diff = mark_price - retrieve_price(i)
    price_percentage_diff = price_diff / mark_price * 100
    return round(price_percentage_diff, 2)
