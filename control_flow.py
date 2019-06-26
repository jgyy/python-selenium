"""
Execute statements repeatedly
Conditions are used to stop the execution of loops
Iterable items are Strings, List, Tuple, Dictionary
"""

if 100 > 10:
    print("Hundred is greater than 10")
VALUE = 'green'
if VALUE == 'green':
    print("Go")
    VALUE += ' red'
elif VALUE == 'yellow':
    print("Prepare to stop")
else:
    print("Stop")
print("It will always print")

X = 0
while X < 10:
    print("Value of x is: " + str(X))
    X += 1
    if X == 8:
        break
    print("This example is awesome")
    print("*"*64)
else:
    print("Just broke out of the loop")
L = []
NUM = 0
while NUM < 8:
    L.append(NUM)
    NUM += 1
    print("Value of num is: " + str(NUM))
print(L)

MY_STRING = 'abcabc'
for c in MY_STRING:
    if c == 'a':
        print("A", end=" ")
    else:
        print(c, end=" ")
print()
CARS = ['bmw', 'benz', 'honda']
for car in CARS:
    print(car)
print("*"*64)
NUMS = [1, 2, 3]
for n in NUMS:
    print(n * 10, end=" ")
print()
D = {'one': 1, 'two': 2, 'three': 3}
for k in D:
    print(k + " " + str(D[k]), end=", ")
print()
for k, v in D.items():
    print(k, v)

L1 = [1, 2, 3]
L2 = [6, 7, 8, 20, 30, 40]
for a, b in zip(L1, L2):
    if a > b:
        print(a)
    else:
        print(b)

print(list(range(0, 10)))
A = range(0, 24, 2)
print(A, type(A), list(A))
for num in range(3):
    print(num)
