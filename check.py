import time

def check():
    while True:
        print("What do you want to check? ")
        print("1. trend")
        print("2. minute")
        print("3. position")
        print("4. realizedPNL")
        input_num = input("\nEnter a number   :   ") or '1'

        if (input_num == '1'):
            start = time.time()
            from get_hour import get_hour
            from get_clear_direction import clear_direction
            get_hour(1)
            get_hour(2)
            get_hour(4)
            clear_direction()
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '2'):
            import get_minute
            loop = input("Do you want to loop? [Y/n]") or 'n'
            if loop == 'Y':
                while True:
                    get_minute.current_minute(1)
                    get_minute.current_minute(5)
                    print()
                    time.sleep(3)
            else:
                start = time.time()
                get_minute.current_minute(1)
                get_minute.current_minute(5)
                print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '3'):
            start = time.time()
            from get_position import get_position_info
            print("\nThe <get_position.py> return value is : " + get_position_info())
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '4'):
            import get_realizedPNL
            break

        else: print("❗Invalid Number❗Try again❗\n")

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
