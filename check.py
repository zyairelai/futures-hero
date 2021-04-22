import config, time
from termcolor import colored

def entry_condition(i):
    import binance_futures, heikin_ashi
    klines_6HOUR = binance_futures.KLINE_INTERVAL_6HOUR(i)
    klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR(i)
    print("DIRECTION")
    heikin_ashi.output_firstrun(klines_6HOUR)
    heikin_ashi.output_previous(klines_6HOUR)
    heikin_ashi.output_current(klines_6HOUR)
    print("\nCONFIRMATION")
    heikin_ashi.output_firstrun(klines_1HOUR)
    heikin_ashi.output_previous(klines_1HOUR)
    heikin_ashi.output_current(klines_1HOUR)

    print("\n6 HOUR VOLUME")
    print("Firstrun Volume  :   " + str(binance_futures.firstrun_volume(klines_6HOUR)))
    print("Previous Volume  :   " + str(binance_futures.previous_volume(klines_6HOUR)))
    print("Current Volume   :   " + str(binance_futures.current_volume(klines_6HOUR)))

def check():
    print("What do you want to check? ")
    print("1. entry condition")
    print("2. minute")
    print("3. position")
    print("4. realizedPNL")
    input_num = input("\nEnter a number   :   ")

    if (input_num == '1'):
        start = time.time()
        for i in range(len(config.pair[i])): entry_condition(i)
        print(f"Time Taken: {time.time() - start} seconds")

    elif (input_num == '2'):
        import binance_futures, heikin_ashi
        loop = input("Do you want to loop? [Y/n]") or 'n'
        if loop == 'Y':
            while True:
                for i in range(len(config.pair[i])): heikin_ashi.output_current(binance_futures.KLINE_INTERVAL_1MINUTE(i))
                print()
                time.sleep(3)
        else:
            start = time.time()
            for i in range(len(config.pair[i])): heikin_ashi.output_current(binance_futures.KLINE_INTERVAL_1MINUTE(i))
            print(f"Time Taken: {time.time() - start} seconds")

    elif (input_num == '3'):
        start = time.time()
        import binance_futures
        from get_position import get_position_info
        for i in range(len(config.pair[i])):
            response = binance_futures.position_information(i)[0]
            print("\nThe <get_position.py> return value is : " + get_position_info(response))
            print(f"Time Taken: {time.time() - start} seconds")

    else: import get_realizedPNL
    print()
try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
