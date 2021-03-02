import time
from termcolor import colored

def check():
    print("What do you want to check? ")
    print("1. entry condition")
    print("2. minute")
    print("3. position")
    print("4. realizedPNL")
    input_num = input("\nEnter a number   :   ")

    if (input_num == '1'):
        start = time.time()
        import heikin_ashi
        heikin_ashi.get_hour(6)
        heikin_ashi.get_hour(4)
        heikin_ashi.get_hour(2)
        heikin_ashi.get_hour(1)

        from binance_futures import get_volume
        previous_volume = get_volume("PREVIOUS", "1HOUR")
        current_volume  = get_volume("CURRENT", "1HOUR")
        print("Previous Volume  :   " + str(previous_volume))
        print("Current  Volume  :   " + str(current_volume))
        
        if (previous_volume / 5) < current_volume: 
            print(colored("Volume Entry     :   YES", "green"))
        else: print(colored("Volume Entry     :   NO", "red"))
        if heikin_ashi.pattern_broken("5MINUTE") == "BROKEN": print(colored("5 min  Volume    :   BROKEN", "red"))
        if heikin_ashi.pattern_broken("1HOUR") == "BROKEN": print(colored("1 hour Volume    :   BROKEN", "red"))

        print(f"Time Taken: {time.time() - start} seconds")

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
            print(f"Time Taken: {time.time() - start} seconds")

    elif (input_num == '3'): 
        start = time.time()
        from get_position import get_position_info
        print("\nThe <get_position.py> return value is : " + get_position_info())
        print(f"Time Taken: {time.time() - start} seconds")

    elif (input_num == '4'): import get_realizedPNL

    else: print(colored("\nINVALID INPUT!", "red"))
    print()
try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
