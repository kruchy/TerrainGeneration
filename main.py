import maps.point as points
from maps.path import *
from maps.grid import *

import json
from graphics import * 
from grid import calcSize


if __name__ == '__main__':
    win = GraphWin("Lines", 1000, 800)
    win.setCoords(0,0,1000,800)
    p1 = points.Point(0.0,0.0)
    p2 = points.Point(90.0,90.0)
    p3 = points.Point(50.0,10.0)
    p4 = points.Point(35.0,50.0)
    p5 = points.Point(50.0,50.0)
    p6 = points.Point(14.0,35.0)
    path= Path()
#     path.addPoint(p3)
#     path.addPoint(p4)
#     path.addPoint(p5)
#     path.addPoint(p6)
    for i in range(1,50,1):
#         path.addPoint(points.Point(i,500-i))
#         path.addPoint(points.Point(i,math.sqrt(360000 - i**2)))
        path.addPoint(points.Point(i,math.fabs(50*math.sin(math.radians(i)))))
        
        
    
#     for i in range(1,10):
#         p = win.getMouse()
#         path.addPoint(points.Point(p.getX(),p.getY()))
    for i in range(0,len(path.pointList)-1):
        line = Line(Point(path.pointList[i].latitude,path.pointList[i].longitude),Point(path.pointList[i+1].latitude,path.pointList[i+1].longitude))
        line.setOutline("red")
        line.draw(win)
        
 
    size = calcSize(path.maxDistance())
    grid = Grid(0.0,0.0,p2.latitude,p2.longitude,0)
    print(grid.toCurve())
    grid.deriveWithPath(path)
    
    for i in grid.toCurve():
        p0 = Point(i[0][0],i[0][1])
        p1 = Point(i[1][0],i[1][1])
        p2 = Point(i[2][0],i[2][1])
        p3 = Point(i[3][0],i[3][1])
        line0 = Line(p0,p1)
        line1 = Line(p1,p2)
        line2 = Line(p2,p3)
        line3 = Line(p3,p0)
        line0.draw(win)
        line1.draw(win)
        line2.draw(win)
        line3.draw(win)
    r = grid.getElevation()
#     response = json.loads('{\n   "results" : [\n      {\n         "elevation" : 4411.94189453125,\n         "location" : {\n            "lat" : 36.578581,\n            "lng" : -118.291994\n         },\n         "resolution" : 19.08790397644043\n      }\n   ],\n   "status" : "OK"\n}\n')
#     for resultset in response['results']:
#         for val in resultset:
#             text = Text(Point(800,600-i),resultset[val])
#             text.draw(win)
#             i = i+30
#     for p in grid.pointList:
#             print(p)
    win.getMouse()
    win.close()

# main()