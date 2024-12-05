# Constants
EPSILON = 1e-10

###
# region Floating point comparisons
###
"""
Equal with tolerance for floating point inaccuracies
"""
def almost_equal(a: float, b: float, epsilon=EPSILON):
    return abs(a - b) < epsilon

"""
More than with tolerance for floating point inaccuracies
"""
def almost_more_than(a: float, b: float, epsilon=EPSILON):
    return a > b + epsilon

"""
Less than with tolerance for floating point inaccuracies
"""
def almost_less_than(a: float, b: float, epsilon=EPSILON):
    return a < b - epsilon

"""
Less than or equal with tolerance for floating point inaccuracies
"""
def almost_less_than_or_equal(a: float, b: float, epsilon=EPSILON):
    return a < b + epsilon

"""
More than or equal with tolerance for floating point inaccuracies
"""
def almost_more_than_or_equal(a: float, b: float, epsilon=EPSILON):
    return a > b - epsilon
# endregion

###
# region Safe division
###
"""
Return 0 instead if we are dividing by 0
"""
def safe_divide(a: float, b: float):
    if b == 0:
        return 0
    
    return a / b

def safe_floor_divide(a: float, b: float):
    if b == 0:
        return 0
    
    return a // b

def safe_mod(a: float, b: float):
    if b == 0:
        return 0
    
    return a % b

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
# endregion