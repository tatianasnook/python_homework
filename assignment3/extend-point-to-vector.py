import math

# Task 5.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __str__(self):
        return f"({self.x}, {self.y})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
class Vector(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


p1 = Point(3, 4)
p2 = Point(3, 4)
p3 = Point(0, 0)
print("Point equality:", p1 == p2)
print("Point string:", str(p1))
print("Distance between p1 and p3:", p1.distance_to(p3))

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print("Vector string:", v1)
print("Vector addition result:", v3)
