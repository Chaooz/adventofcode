
from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_list import *
from advent_libs_vector2 import *

class Polygon:
    points: list[Vector2]
    edges_vertical: list[tuple[float, float, float]]  # x, y_min, y_max
    edges_horizontal: list[tuple[float, float, float]]  # y, x_min, x_max

    def __init__(self, points: list[Vector2]):
        self.points = points
        self.edges_vertical = []
        self.edges_horizontal = []

        lenPoints = len(self.points)
        for i in range(lenPoints):
            vec1 = self.points[i]
            vec2 = self.points[(i + 1) % lenPoints]
            if vec1.x == vec2.x:  # vertical
                self.edges_vertical.append((vec1.x, min(vec1.y, vec2.y), max(vec1.y, vec2.y)))
            else:  # horizontal
                self.edges_horizontal.append((vec1.y, min(vec1.x, vec2.x), max(vec1.x, vec2.x)))

    def isPointInside(self, point: Vector2) -> bool:
        inside = False
        lenPoints = len(self.points)
        for i in range(lenPoints):
            vec1 = self.points[i]
            vec2 = self.points[(i + 1) % lenPoints]
            if (vec1.y > point.y) != (vec2.y > point.y):
                intersect_x = (vec2.x - vec1.x) * (point.y - vec1.y) / (vec2.y - vec1.y) + vec1.x
                if point.x < intersect_x:
                    inside = not inside
        return inside

    def isAreaCrossing(self, minX, minY, maxX, maxY) -> bool:
 
        for vx, vy_min, vy_max in self.edges_vertical:
            if minX < vx < maxX:
                if max(vy_min, minY) < min(vy_max, maxY):
                    return True

        for hy, hx_min, hx_max in self.edges_horizontal:
            if minY < hy < maxY:
                if max(hx_min, minX) < min(hx_max, maxX):
                    return True

        return False

