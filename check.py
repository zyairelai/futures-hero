import time

def check():
    while True:
        print("What do you want to check? ")
        print("1. keys")
        print("2. trend")
        print("3. minute")
        print("4. position")
        print("5. realizedPNL")
        input_num = input("\nEnter a number   :   ") or '1'

        if (input_num == '1'):
            import keys
            print("API OWNER        :   " + keys.api_owner)
            print("API Key          :   " + keys.api_key)
            print("API Secret Key   :   " + keys.api_secret)
            print()
            break

        elif (input_num == '2'):
            start = time.time()
            from get_trend import get_current_trend
            print("\nThe <trend.py> return value is : " + get_current_trend())
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '3'):
            from get_1_minute import get_current_minute
            loop = input("Do you want to loop? [Y/n]") or 'n'
            if loop == 'Y':
                while True:
                    get_current_minute()
                    print()
                    time.sleep(3)
            else:
                start = time.time()
                print("\nThe <minute.py> return value is : " + get_current_minute())
                print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '4'):
            start = time.time()
            from get_position import get_position_info
            print("\nThe <position.py> return value is : " + get_position_info())
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '5'):
            import realizedPNL
            break

        else: print("❗Invalid Number❗Try again❗\n")

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")