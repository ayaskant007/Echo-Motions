with open("Tables.txt", "r") as f:
    data = f.read()


with open("renamed_by_python.txt", "w") as f:
    writer = f.write(data)
