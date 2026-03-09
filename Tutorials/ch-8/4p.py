
def sum(num):
    if num==1:
        return 1
    return (num*(num-1)/2) + num


n = int(input("Enter a number: "))

print(round(sum(n)))