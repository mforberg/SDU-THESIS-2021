def fetch_user_integer(limit:int):
    keyTwo = None
    while True:
        try:
            keyTwo = int(input())
            if limit >= keyTwo:
                break
            else:
                print(f"Please stay within the limit of {limit}")
        except:
            print("Please put in a integer")
    return keyTwo