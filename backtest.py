import config
import strategy
from datetime import datetime

fees = 0.2
cover_fees = False
print_logs = False

def backtest():
    all_pairs = 0
    for i in range(len(config.pair)):
        print(config.pair[i])
        leverage = config.leverage[i]
        hero = strategy.futures_hero(config.pair[i])
        print("Start Time Since " + str(datetime.fromtimestamp(hero["timestamp"].iloc[0]/1000)))
        if print_logs : print(hero)

        long_result = round(check_PNL(hero, leverage, "_LONG"), 2)
        short_reult = round(check_PNL(hero, leverage, "SHORT"), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")

def check_PNL(hero, leverage, positionSide):
    position = False
    total_pnl, total_trades, liquidations = 0, 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "_LONG":
        open_position = "GO_LONG"
        exit_position = "EXIT_LONG"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "GO_SHORT"
        exit_position = "EXIT_SHORT"
        liq_indicator = "high"

    for i in range(len(hero)):
        if not position:
            if hero[open_position].iloc[i]:
                position = True
                entry_price = hero['close'].iloc[i]
        else:
            liquidated = (hero[liq_indicator].iloc[i] - entry_price) / entry_price * 100 * leverage < -80

            if not cover_fees:
                if hero[exit_position].iloc[i] or liquidated:
                    position = False

                    if liquidated:
                        realized_pnl = -100
                        liquidations = liquidations + 1
                    else: realized_pnl = ((hero['close'].iloc[i] - entry_price) / entry_price * 100 * leverage) - (fees * leverage)

                    if realized_pnl > fees * leverage: wintrade = wintrade + 1
                    else: losetrade = losetrade + 1

                    total_trades = total_trades + 1
                    total_pnl = total_pnl + realized_pnl
            else:
                unrealizedPNL = (hero['close'].iloc[i] - entry_price) / entry_price * 100 * leverage
                breakeven_PNL = fees * leverage

                if (hero[exit_position].iloc[i] and unrealizedPNL > breakeven_PNL) or liquidated:
                    position = False

                    if liquidated:
                        realized_pnl = -100
                        liquidations = liquidations + 1
                    else: realized_pnl = ((hero['close'].iloc[i] - entry_price) / entry_price * 100 * leverage) - (fees * leverage)

                    if realized_pnl > fees * leverage: wintrade = wintrade + 1
                    else: losetrade = losetrade + 1

                    total_trades = total_trades + 1
                    total_pnl = total_pnl + realized_pnl

    if total_pnl != 0:
        print("PNL for " + positionSide + " Positions: " + str(round(total_pnl, 2)) + "%")
        print("Total  Executed  Trades: " + str(round(total_trades, 2)))
        print("Total Liquidated Trades: " + str(round(liquidations)))
        print("_Win Trades: " + str(wintrade))
        print("Lose Trades: " + str(losetrade))
        if (wintrade + losetrade > 1):
            winrate = round(wintrade / (wintrade + losetrade) * 100)
            print("Winrate : " + str(winrate) + " %")
        print()

    return round(total_pnl, 2)

backtest()