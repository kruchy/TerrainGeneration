import maps.point as points
from maps.path import Path
from maps.grid import Grid,derive

p1 = points.Point(1.0,2.0)
p2 = points.Point(2.0,3.0)
path= Path()
path.addPoint(1)


grid = Grid(p1.latitude,p1.longitude,p2.latitude,p2.longitude,0)

print(points.distance(p1,p2))
print(p1)
print(path)
print(path.pointList[0])  
print(grid.toCurve())  

grid = derive(grid)
# 
# print(derive(grid).toCurve())
# print(derive(derive(grid)).toCurve())
print(grid.toCurve())
grid = derive(grid)

print(grid.toCurve())