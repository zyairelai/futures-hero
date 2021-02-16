import time

def check():
    print("What do you want to check? ")
    print("1. trend")
    print("2. minute")
    print("3. position")
    print("4. realizedPNL")
    input_num = input("\nEnter a number   :   ")

    if (input_num == '1'):
        start = time.time()
        import heikin_ashi
        heikin_ashi.get_hour(1)
        heikin_ashi.get_hour(2)
        heikin_ashi.get_hour(4)
        heikin_ashi.get_clear_direction()
        print(f"Time Taken: {time.time() - start} seconds\n")

    if (input_num == '2'):
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
        start = time.time()
        from get_position import get_position_info
        print("\nThe <get_position.py> return value is : " + get_position_info())
        print(f"Time Taken: {time.time() - start} seconds\n")

    else: import get_realizedPNL

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
