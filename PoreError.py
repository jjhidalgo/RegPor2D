"""Exception managing for RegPore2D."""

class PoreError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self):
        """ Does nothing"""
        Exception.__init__()

class ErrorPacking(PoreError):
    """Exception raised for errors in the packing.

    The only allowed packings are:
        tri -- triangular
        sqr  -- square
        etri -- elongated triangular
    """
    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        print "Wrong packing!"

class ErrorNx(PoreError):
    """Exception raised for nx!
    It is negative or an even number with tri and etri packings."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        msg = "Number of grains in x direction too small, negative,"
        msg = msg + "or even with tri and etri packings!"
        print msg

class ErrorNy(PoreError):
    """Exception raised for ny<1  or nx*radius>1.0!"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        print "Number of grains in y direction too small or negative!"

class ErrorRadius(PoreError):
    """Exception raised for grain radius. Raduis <1e-9 or Radius >1"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        print "Grain radius too small or negative!"

class ErrorThroatNegative(PoreError):
    """Exception raised for pore throat. Pore throat is negative"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        print "Pore throat negative! Check number of grains in y and radius."

class ErrorNotPorousMedium(PoreError):
    """Exception when an variable is not an instance of RegPore2D."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__()
        msg = "A porous medium (instance of RegPore2D"
        msg = msg + " is needed for this operation."
        print msg
