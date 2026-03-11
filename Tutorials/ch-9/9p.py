with open("poem.txt", "r") as f:
    data = f.read()

with open("this.txt", "r") as w:
    datacheck = w.read()

if data in datacheck:
    print("This file has the same content.")
else:
    print("Files have differing content.")