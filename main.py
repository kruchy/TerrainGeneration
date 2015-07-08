from maps.point import Point
from maps.path import Path

p = Point(1,2)
path= Path()
path.addPoint(p)

print(p)
print(path)
print(path.pointList[0])