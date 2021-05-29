import os
from termcolor import colored

def check_path():
    tested_pair = []
    backtest_pairs = os.listdir("BACKTEST")
    for pair in backtest_pairs:
        if os.path.isfile(os.path.join("BACKTEST", pair, "PNL.txt")):
            tested_pair.append(pair)
    if tested_pair == []: NO_DATA()
    return tested_pair

def calculate_PnL():
    tested_pair = check_path()
    for pair in tested_pair:
        total, liquidations, executed_trades = 0, 0, 0
        with open((os.path.join("BACKTEST", pair, "PNL.txt")), "r", encoding="utf-8") as input_file:
            for line in input_file:
                total = round(total + float(line), 2)
                executed_trades = executed_trades + 1
                if float(line) < 0: liquidations = liquidations + 1

            print(pair)
            print("Executed Trades :  " + str(executed_trades))
            print("Liquidations    :  " + str(liquidations))
            if total > 0: print(colored('Overall PNL     : {} USDT'.format(total), "green"))
            else: print(colored('Overall PNL     : {} USDT'.format(total), "red"))
            print()

def NO_DATA(): print("\nThere is no backtest data.\n")
if not os.path.exists("BACKTEST"): NO_DATA()
else: calculate_PnL()
