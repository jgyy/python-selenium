"""
Exceptions are errors
We should handle exceptions in our code to make sure the code is working the way we want and is
handling all the unwanted issues.
Link to 3.5 build-in exceptions. - https://docs.python.org/3/library/exceptions.html
"""


def exception_handling():
    """
    Showing 2 excep handling
    """
    try:
        car = {
            "make": "bmw",
            "model": "550i",
            "year": "2016"
        }
        val_a = 10
        val_b = 20
        val_c = 0
        val_d = val_a + val_b
        val_d /= val_c
        print(val_d, car["color"])
    except ZeroDivisionError:
        print("Zero Division")
    except TypeError:
        print("Can't add string to integer")
    except KeyError:
        print("Key not found")
    else:
        print("Because there was no exception, else is executed")
    finally:
        print("Finally, always executed")


exception_handling()
