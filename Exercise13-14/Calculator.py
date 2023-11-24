## Ex 13 - Q 02
class Calculator:
    ## Methods:
    add = lambda self, x, y : x + y
    subtract = lambda self, x, y : x - y
    multiply = lambda self, x, y : x * y
    divide = lambda self, x, y : x/y if y != 0 else "Cannot divide by zero"

c = Calculator() # an object of `Calculator` class
x, y = 15, 5
print(f"{x} + {y} = {c.add(x, y)}")
print(f"{x} - {y} = {c.subtract(x, y)}")
print(f"{x} x {y} = {c.multiply(x, y)}")
print(f"{x} / {y} = {c.divide(x, y)}")