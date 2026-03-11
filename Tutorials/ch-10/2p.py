class Calculator:

    def __init__(self, n):
        self.n = n

    def square(self):
        print(f"The square of the number is {self.n*self.n}")

    def cube(self):
        print(f"The cube of the number is {self.n*self.n*self.n}")
    
    def squareroot(self):
        print(f"The square root of the number is {self.n**1/2}")

a = Calculator(int(input("Enter a number: ")))
operation = input("Enter a operation: ")
if operation=="square":
    a.square()
elif operation=="sqroot":
    a.squareroot()
else:
    a.cube()
