

with open("log.txt", "r") as f:
    lines = f.readlines()


lineno=1
for line in lines:
        if "Python" in line:
            print(f"Python found! {lineno}")
            break
            lineno+=1