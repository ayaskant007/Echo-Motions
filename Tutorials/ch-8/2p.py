'''
Formula C to F
F = 9C/5
'''

Celsius = int(input("Enter your temperature in Celsius: "))

def convert():
    return (9/5 * Celsius) + 32 

print(round(convert()))