import heikin_ashi, binance_futures

i = 0

binance_futures.change_to_hedge_mode()

print(binance_futures.get_current_position_mode())