def table(num, end):
    for i in range(1, end+1):
        print(num * i)

num=int(input("Enter a number:  "))
end = int(input("Enter a number till where you want the table to be printed:  "))

table(num, end)
    