
for i in range(2, 21):
    for x in range(1, 11):
        f = open("Tables.txt", "a")
        product = i*x
        f.write(f"The table of {i} is\n {i} X {x} = {product} ")
        f.close()
