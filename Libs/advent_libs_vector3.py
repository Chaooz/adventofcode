
import dataclasses as dc

from advent_libs_vector2 import Vector2
@dc.dataclass(frozen=True)
class Vector3:
    x:int
    y:int
    z:int

    def Duplicate(self):
        return Vector3(self.x,self.y,self.z)       

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector3(x,y,z)

    def __mul__(self, other):
        if isinstance(other, Vector3 ):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vector3(x,y,z)

    def __truediv__(self, other):
        if isinstance(other, Vector3 ):
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        else:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        return Vector3(x,y,z)

    def Normalize(self) :
        x = self.x
        y = self.y
        z = self.z
        if x > 0: x = 1
        if x < 0: x = -1
        if y > 0: y = 1
        if y < 0: y = -1
        if z > 0: z = 1
        if z < 0: z = -1
        if x == 0 and y == 0 and z == 0:
            print("BUG!" + self.ToString())
        return Vector3(x,y,z)
    
    def Distance(self, other) :
        diff = self - other

        x = other.x - self.x
        y = other.y - self.y
        z = other.z - self.z

        # Formula SQRT(a^2 + b^2 + c^2)
        dist = (x ** 2 + y ** 2 + z ** 2) ** 0.5

        return dist
    
    def Tuple(self) :
        return (self.x,self.y,self.z)

    def IsZero(self):
        return self.x == 0 and self.y == 0 and self.z == 0

    def sortHelper(vector):
        return vector.x

    def rot(self, facing:int):
        x = self.y * facing
        y = self.x * facing
        z = self.z * facing
        return Vector3(x,y,z)

    def rotateLeft(self):
        return Vector3(self.y,-self.x,self.z)
    def rotateRight(self):
        return Vector3(-self.y,self.x,self.z)

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
        z = self.z + other.z
        sum = Vector3(x,y,z)
#        print("Vec2.add:" + self.ToString() + " + " + other.ToString() + " = " + sum.ToString())
        return sum 

    def Divide(self, other):
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Vector3(x,y,z)
   
    def ToString(self):
        return "" + str(self.x) + "x" + str(self.y) + "x" + str(self.z)