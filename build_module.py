"""
https://docs.python.org/3/library/
"""
import math
from math import sqrt


class ModulesMath:
    """
    Simple Math Practice Modules
    """

    def __init__(self, number):
        self.number = number
        self.make = ""
        self.model = ""

    def square_root(self):
        """
        square root of number
        """
        print(sqrt(self.number))

    def number_square(self):
        """
        number power of 2
        """
        print(math.pow(self.number, 2))

    def car_description(self):
        """
        Add in car descriptions
        """
        self.make = "bmw"
        self.model = "550i"


M = ModulesMath(100)
M.square_root()
M.number_square()
M.car_description()
print(M.make, M.model)
