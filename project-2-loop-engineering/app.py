"""app.py - Fixed functions."""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def abs_value(x):
    """Return the absolute value of x."""
    return abs(x)


def safe_divide(a, b):
    """Return a / b, or None if b is 0."""
    if b == 0:
        return None
    return a / b
