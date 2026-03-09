'''
fact(0) =1
fact(1) = 1
factorial(5) = 5x4x3x2x1
factorial(5) = 5x4x3x2x1
factorial(5) = 5x4x3x2x1
factorial(5) = 5x4x3x2x1
factorial(5) = 5x4x3x2x1
'''

def factorial(n):
    if (n==1 or n==0):
        return 1
    return n * factorial(n-1)

n = int(input("Enter a number: "))

print(f"Factorial of {n} is {factorial(n)}")