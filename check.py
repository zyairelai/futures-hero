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
            from get_trend import get_hour
            get_hour()
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '2'):
            from get_minute import recent_minute
            loop = input("Do you want to loop? [Y/n]") or 'n'
            if loop == 'Y':
                while True:
                    recent_minute()
                    print()
                    time.sleep(3)
            else:
                start = time.time()
                print("\nThe <get_minute.py> return value is : " + recent_minute())
                print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '3'):
            start = time.time()
            from get_position import get_position_info
            print("\nThe <get_position.py> return value is : " + get_position_info())
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '4'):
            import realizedPNL
            break

        else: print("❗Invalid Number❗Try again❗\n")

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
