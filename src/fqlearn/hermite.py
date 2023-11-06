import math

import numpy as np

"""
These are functions that are used to perform Hermite's 
monotonic cubic interpolation.
For more info check 
https://en.wikipedia.org/wiki/Monotone_cubic_interpolation
"""


def h00(t: float) -> float:
    """
    First Hermite monotonic cubic interpolation polynomial.

    Parameters
    ----------
    t : float
        Independent variable.

    Returns
    ------
    h00 : float
        returns 2t^3 - 3t^2 + 1
        evaluated at t.
    """
    h00 = 2 * t**3 - 3 * t**2 + 1

    return h00


def h10(t: float) -> float:
    """
    Second Hermite monotonic cubic interpolation polynomial.

    Parameters
    ----------
    t : float
        Independent variable.

    Returns
    ------
    h10 : float
        returns t^3 - 2t^2 + t
        evaluated at t.
    """

    h10 = t**3 - 2 * t**2 + t

    return h10


def h01(t: float) -> float:
    """
    Third Hermite monotonic cubic interpolation polynomial.

    Parameters
    ----------
    t : float
        Independent variable.

    Returns
    ------
    h01 : float
        returns -2t^3 + 3t^2
        evaluated at t.
    """

    h01 = -2 * t**3 + 3 * t**2
    return h01


def h11(t: float) -> float:
    """
    Fourth Hermite monotonic cubic interpolation polynomial.

    Parameters
    ----------
    t : float
        Independent variable

    Returns
    -------
    h11 : float
        returns t^3 - t^2
        evaluated at t
    """

    h11 = t**3 - t**2
    return h11


# TODO: Complete docstring check numpy arrays type
def pchint(x, y, x0):
    """
    An python code to implement Hermite monotonic cubic interpolation.

    Parameters
    ----------
    x0 : List[float]
        List of values to interpolate.
    x : List [float]
        List of values in x axis used to perform interpolation
    y : List[float]
        List of values in y axis used to perform interpolation

    Returns
    -------
    y : List[float]
        A list of interpolated values
    """

    n = len(x)
    d = np.zeros(n - 1)

    # Calculating the first numerical derivatives
    # store it in `d`
    for i in range(n - 1):
        d[i] = (y[i + 1] - y[i]) / (x[i + 1] - x[i])

    m = np.zeros(n)
    m[0] = d[0]
    m[-1] = d[-1]

    for i in range(1, n - 1):
        if d[i - 1] * d[i] < 0:
            m[i] = 0
        else:
            m[i] = (d[i - 1] + d[i]) / 2

    for i in range(n - 1):
        if y[i] == y[i + 1]:
            m[i] = 0
            m[i + 1] = 0

    for i in range(n - 1):
        if m[i] != 0:
            alfa = m[i] / d[i]
            beta = m[i + 1] / d[i]

            condition = alfa - ((2 * alfa + beta - 3) ** 2) / (alfa + beta - 2) / 3

            while condition < 0:
                tau = 3 / math.sqrt(alfa**2 + beta**2)
                alfa = tau * alfa
                beta = tau * beta
                m[i] = alfa * d[i]
                m[i + 1] = beta * d[i]
                condition = alfa - ((2 * alfa + beta - 3) ** 2) / (alfa + beta - 2) / 3
    pos = 0
    c = 0
    y = np.zeros(len(x0))

    for xi in x0:
        if xi > x[pos + 1]:
            pos += 1

        delta = x[pos + 1] - x[pos]
        t = (xi - x[pos]) / delta
        y[c] = (
            y[pos] * h00(t)
            + delta * m[pos] * h10(t)
            + y[pos + 1] * h01(t)
            + delta * m[pos + 1] * h11(t)
        )
        c += 1

    return y
