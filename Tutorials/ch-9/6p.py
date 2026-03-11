with open("log.txt", "r") as f:
    data = f.read()
    if "Python" in data:
        print("Python found!")