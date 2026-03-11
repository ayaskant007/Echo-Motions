with open("this.txt", "r") as f:
    data = f.read()

with open("thiscopy.txt", "w") as w:
    datacopy = w.write(data)