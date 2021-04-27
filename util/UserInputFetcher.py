def fetch_user_integer_with_limit(limit: int):
    keyTwo = None
    while True:
        try:
            keyTwo = int(input())
            if limit >= keyTwo >= 0:
                break
            else:
                print(f"Please stay within the limit of {limit}")
        except:
            print("Please put in a integer")
    return keyTwo


def fetch_user_integer():
    keyTwo = None
    while True:
        try:
            keyTwo = int(input())
            break
        except:
            print("Please put in a integer")
    return keyTwo