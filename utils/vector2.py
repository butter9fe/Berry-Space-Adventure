from utils.math_extensions import *
import math

"""
Custom Vector2 'type'
Essentially just a class that stores numeric x,y values

The remaining rest of the function just overloads operators to allow for Mathmatical manipulation
"""
class Vector2():
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    ### Custom Vector2 Manipulation
    def set_zero(self):
        self.x = 0
        self.y = 0

    def is_zero(self):
        return almost_equal(self.x, 0) and almost_equal(self.y, 0)
    
    def normalized(self):
        return self / self.length()
    
    """
    Returns the length (magnitude) squared of vector
    Squared length is faster to calculate that square-root, so use this if you don't need the actual length
    """
    def length_squared(self):
        return self.x * self.x + self.y * self.y
    
    """
    Returns the actual length (magnitude) of vector
    """
    def length(self):
        return math.sqrt(self.length_squared())
    
    """
    Returns the distance between the current vector and the other vector
    """
    def distance(self, other):
        if not isinstance(other, Vector2): # Type checking
            print("other is not Vector2")
            return None
        
        return (self - other).length()
    
    """
    Distance squared between the current vector and the other vector
    Faster calculation.
    """
    def distance_squared(self, other):
        if not isinstance(other, Vector2): # Type checking
            print("other is not Vector2")
            return None
        
        return (self - other).length_squared()
    
    """
    Dot product between two vectors
    """
    def dot(self, other):
        if not isinstance(other, Vector2): # Type checking
            print("other is not Vector2")
            return None
         
        return self.x * other.x + self.y * other.y
    
    ###
    ### Overloaded operators
    ### Reference: https://www.geeksforgeeks.org/operator-overloading-in-python/
    ###
    # region Binary Operators
    ###
    """
    Add operator (ie. a + b)
    """
    """
    Add operator (ie. a + b)
    """
    def __add__(self, other):
        if isinstance(other, Vector2): # If Vector2, add each component
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):# If scalar, add each component by scalar
            return Vector2(self.x + other, self.y + other)
    
    """
    Subtract operator (ie. a - b)
    """
    def __sub__(self, other):
        if isinstance(other, Vector2): # If Vector2, subtract by each component
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):# If scalar, subtract each component by scalar
            return Vector2(self.x - other, self.y - other)
    
    """
    Multiply operator (ie. a * b)
    """
    def __mul__(self, other):
        if isinstance(other, Vector2): # If Vector2, multiply by each component
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):# If scalar, multiply each component by scalar
            return Vector2(self.x * other, self.y * other)
    
    """
    Divide operator (ie. a / b)
    """
    def __truediv__(self, other):
        if isinstance(other, Vector2): # If Vector2, divide by each component
            return Vector2(safe_divide(self.x, other.x), safe_divide(self.y, other.y))
        elif isinstance(other, (int, float)): # If scalar, divide each component by scalar
            return Vector2(safe_divide(self.x, other), safe_divide(self.y, other))
    
    """
    Floor division operator (ie. a // b)
    """
    def __floordiv__(self, other):
        if isinstance(other, Vector2): # If Vector2, floor divide by each component
            return Vector2(safe_floor_divide(self.x, other.x), safe_floor_divide(self.y, other.y))
        elif isinstance(other, (int, float)): # If scalar, floor divide each component by scalar
            return Vector2(safe_floor_divide(self.x, other), safe_floor_divide(self.y, other))
    
    """
    Modulo operator (ie. a % b)
    """
    def __mod__(self, other):
        if isinstance(other, Vector2): # If Vector2, modulo by each component
            return Vector2(safe_mod(self.x, other.x), safe_mod(self.y, other.y))
        elif isinstance(other, (int, float)):# If scalar, modulo each component by scalar
            return Vector2(safe_mod(self.x, other), safe_mod(self.y, other))
    
    """
    Power operator (ie. a ** b)
    """
    def __pow__(self, other):
        if isinstance(other, Vector2): # If Vector2, power each component
            return Vector2(self.x ** other.x, self.y ** other.y)
        elif isinstance(other, (int, float)): # If scalar, power each component by scalar
            return Vector2(self.x ** other, self.y ** other)
    
    """
    Negative operator (ie. -a)
    """
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    # endregion
    
    ###
    # region Comparison Operators
    ###
    """
    Equality operator (ie. a == b)
    """
    def __eq__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False

        return almost_equal(self.x, other.x) and almost_equal(self.y, other.y)
    
    """
    Inequality operator (ie. a != b)
    """
    def __ne__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False
        
        return not almost_equal(self, other) or not almost_equal(self.y, other.y)
    
    """
    Less than operator (ie. a < b)
    """
    def __lt__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False
        
        return almost_less_than(self.x, other.x) and almost_less_than(self.y, other.y)
    
    """
    Less than or equal operator (ie. a <= b)
    """
    def __le__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False
        
        return almost_less_than_or_equal(self.x, other.x) and almost_less_than_or_equal(self.y, other.y)
    
    """
    Greater than operator (ie. a > b)
    """
    def __gt__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False
        
        return almost_more_than(self.x, other.x) and almost_more_than(self.y, other.y)
    
    """
    Greater than or equal operator (ie. a >= b)
    """
    def __ge__(self, other):
        if not isinstance(other, Vector2): # Type checking
            return False
        
        return almost_more_than_or_equal(self.x, other.x) and almost_more_than_or_equal(self.y, other.y)
    # endregion

    ###
    # region Assignment Operators
    ###
    """
    Addition assignment operator (ie. a += b)
    """
    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
        return self

    """
    Subtraction assignment operator (ie. a -= b)
    """
    def __isub__(self, other):
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
        return self

    """
    Multiplication assignment operator (ie. a *= b)
    """
    def __imul__(self, other):
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
        return self

    """
    Division assignment operator (ie. a /= b)
    """
    def __itruediv__(self, other):
        if isinstance(other, Vector2):
            self.x = safe_divide(self.x, other.x)
            self.y = safe_divide(self.y, other.y)
        elif isinstance(other, (int, float)):
            self.x = safe_divide(self.x, other)
            self.y = safe_divide(self.y, other)
        return self

    """
    Floor division assignment operator (ie. a //= b)
    """
    def __ifloordiv__(self, other):
        if isinstance(other, Vector2):
            self.x = safe_floor_divide(self.x, other.x)
            self.y = safe_floor_divide(self.y, other.y)
        elif isinstance(other, (int, float)):
            self.x = safe_floor_divide(self.x, other)
            self.y = safe_floor_divide(self.y, other)
        return self

    """
    Modulo assignment operator (ie. a %= b)
    """
    def __imod__(self, other):
        if isinstance(other, Vector2):
            self.x = safe_mod(self.x, other.x)
            self.y = safe_mod(self.y, other.y)
        elif isinstance(other, (int, float)):
            self.x = safe_mod(self.x, other)
            self.y = safe_mod(self.y, other)
        return self

    """
    Power assignment operator (ie. a **= b)
    """
    def __ipow__(self, other):
        if isinstance(other, Vector2):
            self.x **= other.x
            self.y **= other.y
        elif isinstance(other, (int, float)):
            self.x **= other
            self.y **= other
        return self
    
    # endregion
    

