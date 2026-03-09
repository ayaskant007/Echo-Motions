'''
***
**
*

n = 3

'''

def func(n):
    if n==0:
        return
    print("*" * n)
    func(n-1)


n = int(input("Enter a number: "))
func(n)