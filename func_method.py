"""
A group of code statements which can perform some specific task
Methods are reusable and can be called when needed in the code
"""


def sum_nums(n_1=2, n_2=4):
    """
    Get sum of two numbers
    :param n_1: first number
    :param n_2: second number
    """
    return n_1 + n_2


def is_metro(city):
    """
    :param city: city name
    :return: matching city or not
    """
    location = ['sfo', 'nyc', 'la']
    if city in location:
        return True
    return False


def test_method(int_a):
    """
    :param int_a: a number
    """
    print("Value of local 'a' is: " + str(int_a))
    int_a = 2
    print("New value of local 'a' is: " + str(int_a))


def largest_num(*args):
    """largest number"""
    return max(args)


def smallest_num(*args):
    """smallest number"""
    return min(args)


def abs_function(absolute):
    """absolute function"""
    return abs(absolute)


def calculate_net_income(gross, state):
    """
    Calculate the net income after federal and state tax
    :param gross: Gross Income
    :param state: State Name
    :return: Net Income
    """
    state_tax = {'CA': 10, 'NY': 9, 'TX': 0, 'NJ': 6}
    net = gross - (gross * 0.1)
    if state in state_tax:
        net = net - (gross * state_tax[state] / 100)
        print("Your net income after all the heavy taxes is: " + str(net))
        return net
    else:
        print("State not in the list")
        return None


A = 10
print("Value of global 'A' is: " + str(A))
test_method(A)
print("Did the value of global 'A' change? " + str(A))
SUM1 = sum_nums(n_1=4, n_2=9)
SUM2 = sum_nums(21, 18)
SUM3 = sum_nums()
L = [1, 2, 3, 4]
print(SUM1, SUM2, SUM3, L.append(5))
print(L, len(L))
X = is_metro('boston')
print(X)
print(
    largest_num(1, 2, 3, 4),
    smallest_num(23, 5667, 123, 11),
    abs_function(-9343),
    type(99), type(99.9), type("99.9"), type([1, 2, 3])
)
calculate_net_income(100000, 'CA')
