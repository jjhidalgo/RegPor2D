class PoreError(Exception):
    """Base class for exceptions in this module.
       This class manages the errors for RegPore2D."""
    pass

class ErrorPacking(PoreError):
    """Exception raised for errors in the packing.

    The only allowed packings are:
        tri -- triangular
        sqr  -- square
        etri -- elongated triangular
    """

    def __init__(self):
        print("Wrong packing!")

class ErrorNx(PoreError):
    """Exception raised for nx! 
    It is negative or an even number with tri and etri packings."""

    def __init__(self):
        str = "Number of grains in x direction too small, negative,"
        str = str + "or even with tri and etri packings!" 
        print(str)

class ErrorNy(PoreError):
    """Exception raised for ny<1  or nx*radius>1.0!"""

    def __init__(self):
        print("Number of grains in y direction too small or negative!")

class ErrorRadius(PoreError):
    """Exception raised for grain radius. Raduis <1e-9 or Radius >1"""

    def __init__(self):
        print("Grain radius too small or negative!")

class ErrorThroatNegative(PoreError):
    """Exception raised for pore throat. Pore throat is negative"""

    def __init__(self):
        print("Pore throat negative! Check number of grains in y and radius.")


