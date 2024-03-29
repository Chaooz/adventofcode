
class Vector2:
    x:int
    y:int

    def __init__(self, input1 = None, input2 = None ):
        if isinstance(input1, Vector2):
            self.x = input1.x
            self.y = input1.y
        elif isinstance(input1,int) and isinstance(input2,int):
            self.x = input1
            self.y = input2
        else:
            self.x = 0
            self.y = 0
       

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x,y)

    def __mul__(self, other):
        if isinstance(other, Vector2 ):
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = self.x * other
            y = self.y * other
        return Vector2(x,y)

    def __truediv__(self, other):
        if isinstance(other, Vector2 ):
            x = self.x / other.x
            y = self.y / other.y
        else:
            x = self.x / other
            y = self.y / other
        return Vector2(x,y)

    def Normalize(self) :
        if self.x > 0: self.x = 1
        if self.x < 0: self.x = -1
        if self.y > 0: self.y = 1
        if self.y < 0: self.y = -1
        if self.x == 0 and self.y == 0:
            print("BUG!" + self.ToString())
        return self
    
    def Tuple(self) :
        return (self.x,self.y)

    def IsZero(self):
        return self.x == 0 and self.y == 0

    def sortHelper(vector):
        return vector.x

    # def __gt__
    # def __eq__

# +	__add__(self, other)
# –	__sub__(self, other)
# *	__mul__(self, other)
# /	__truediv__(self, other)
# //	__floordiv__(self, other)
# %	__mod__(self, other)
# **	__pow__(self, other)
# >>	__rshift__(self, other)
# <<	__lshift__(self, other)
# &	__and__(self, other)
# |	__or__(self, other)
# ^	__xor__(self, other)


    def __add__(self, other ):
        x = self.x + other.x
        y = self.y + other.y
        sum = Vector2(x,y)
#        print("Vec2.add:" + self.ToString() + " + " + other.ToString() + " = " + sum.ToString())
        return sum 

    def Divide(self, other):
        x = self.x / other.x
        y = self.y / other.y
        return Vector2(x,y)
   
    def ToString(self):
        return "" + str(self.x) + "x" + str(self.y)