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
            input_hour = input("Enter hour (1, 2, 4, 6) : ") or 6
            print("\nThe <get_trend.py> return value is : " + get_hour(int(input_hour)))
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '2'):
            from get_minute import get_current_minute
            loop = input("Do you want to loop? [Y/n]") or 'n'
            if loop == 'Y':
                while True:
                    get_current_minute()
                    print()
                    time.sleep(3)
            else:
                start = time.time()
                print("\nThe <get_minute.py> return value is : " + get_current_minute())
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
