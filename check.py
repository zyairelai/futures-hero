import time
from termcolor import colored

def check():
    print("What do you want to check? ")
    print("1. trend")
    print("2. minute")
    print("3. entry condition")
    print("4. position")
    print("5. realizedPNL")
    input_num = input("\nEnter a number   :   ")

    if (input_num == '1'):
        start = time.time()
        import heikin_ashi
        heikin_ashi.get_hour(1)
        heikin_ashi.get_hour(2)
        heikin_ashi.get_hour(4)
        trend = heikin_ashi.get_clear_direction(6)
        print("The current trend is : " + trend)
        print(f"Time Taken: {time.time() - start} seconds\n")

    elif (input_num == '2'):
        import heikin_ashi
        loop = input("Do you want to loop? [Y/n]") or 'n'
        if loop == 'Y':
            while True:
                heikin_ashi.get_current_minute(1)
                heikin_ashi.get_current_minute(5)
                print()
                time.sleep(3)
        else:
            start = time.time()
            heikin_ashi.get_current_minute(1)
            heikin_ashi.get_current_minute(5)
            print(f"Time Taken: {time.time() - start} seconds\n")

    elif (input_num == '3'): 
        from heikin_ashi import pattern_broken
        from binance_futures import get_volume
        previous_volume = get_volume("PREVIOUS", "1HOUR")
        current_volume  = get_volume("CURRENT", "1HOUR")
        print("Previous Volume  :   " + str(previous_volume))
        print("Current  Volume  :   " + str(current_volume))
        if (previous_volume / 5) < current_volume: print("Volume Entry     :   YES")
        else: print("Volume Entry     :   NO")
        if pattern_broken("5MINUTE") == "BROKEN": print("5 min  Volume    :   BROKEN")
        if pattern_broken("1HOUR") == "BROKEN": print("1 hour Volume    :   BROKEN")

    elif (input_num == '4'):
        start = time.time()
        from get_position import get_position_info
        print("\nThe <get_position.py> return value is : " + get_position_info())
        print(f"Time Taken: {time.time() - start} seconds\n")

    elif (input_num == '5'): import get_realizedPNL

    else: print(colored("\nINVALID INPUT!\n", "red"))

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
