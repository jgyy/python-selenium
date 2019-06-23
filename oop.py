"""
Object Oriented Programming
"""


class Car:
    """Car"""
    wheels = 4

    def __init__(self, make, model="550i"):
        print("You just created the car instance")
        self.make = make
        self.model = model

    def info(self):
        """
        Print out the car information
        """
        print("Make of the car: " + self.make)
        print("Model of the car: " + self.model)

    def drive(self):
        """Driving Car"""
        print(self.make + " car started...")

    def price(self):
        """Car Price"""
        print(self.make + " car cost a lot")


class BMW(Car):
    """BMW"""

    def __init__(self):
        Car.__init__(self, 'BMW')
        print("You Just created the BMW instance")

    def drive(self):
        """Driving Car"""
        super(BMW, self).drive()
        print("You are driving a " + self.make + ", Enjoy...")

    def stop(self):
        """Stopping the Car"""
        print(self.make + " car stopped")

    def headsup_display(self):
        """Turning on the car light"""
        print(self.make + " car: This is a unique feature")


class Fruit:
    """Fruits"""
    fruit = "Fruit: "

    def __init__(self):
        print("I am a fruit")

    def nutrition(self):
        """Nutrition"""
        print(self.fruit + "I am full of vitamins")

    def fruit_shape(self):
        """Shape of the fruit"""
        print(self.fruit + "Every fruit can have different shape")


class Orange(Fruit):
    """Orange fruit"""

    def __init__(self):
        Fruit.__init__(self)
        print("I am Orange")

    def nutrition(self):
        """Nutrition"""
        print(self.fruit + "I am full of vitamin c")

    def color(self):
        """Color of the fruit"""
        print(self.fruit + "I keep it simple, the color is also orange")


FRUIT = Fruit()
FRUIT.nutrition()
FRUIT.fruit_shape()
ORANGE = Orange()
ORANGE.nutrition()
ORANGE.fruit_shape()
ORANGE.color()

print(Car.wheels)
C1 = Car('bmw', '55')
C2 = BMW()
C1.info()
C1.price()
C2.drive()
C2.stop()
C2.headsup_display()
