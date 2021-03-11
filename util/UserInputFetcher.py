def fetch_user_integer():
    keyTwo = None
    while True:
        try:
            keyTwo = int(input())
            break
        except:
            print("Please put in a integer")
    return keyTwo