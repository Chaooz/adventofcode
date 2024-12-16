
import dataclasses as dc
@dc.dataclass(frozen=True)
class Vector2:
    x:int
    y:int

    def Duplicate(self):
        return Vector2(self.x,self.y)       

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
        x = self.x
        y = self.y
        if x > 0: x = 1
        if x < 0: x = -1
        if y > 0: y = 1
        if y < 0: y = -1
        if x == 0 and y == 0:
            print("BUG!" + self.ToString())
        return Vector2(x,y)
    
    def Tuple(self) :
        return (self.x,self.y)

    def IsZero(self):
        return self.x == 0 and self.y == 0

    def sortHelper(vector):
        return vector.x

    def rot(self, facing:int):
        x = self.y * facing
        y = self.x * facing
        return Vector2(x,y)

    def rotateLeft(self):
        return Vector2(self.y,-self.x)
    def rotateRight(self):
        return Vector2(-self.y,self.x)

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