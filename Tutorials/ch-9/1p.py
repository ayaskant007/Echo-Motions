with open("poem.txt") as f:
    data = f.read()
    # print(data)
    if("Twinkle," in data):
        print("The word Twinkle has been found in the data successfully.")
