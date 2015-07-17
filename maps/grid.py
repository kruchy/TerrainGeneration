from point import Point
import utils
import math
import pickle
import urllib3
import datetime
import os
import glob
import simplejson
from time import sleep
from utils import float_equal, calcSize

KEY = 'AIzaSyD4YJdwmlO6sIyJ94egzfy3TLfaai4faAY'
ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
MAXLEVEL = 5
FILENAME = "cache"

class Grid:
    detailLevel = 0
    #coordinates
    #south west corner
    left = Point(0,0)
    #north east corner
    right = Point(0,0)
    pointList = set([])
    
    #children grids
    northWest,southWest,southEast,northEast = 0,0,0,0
    
    def __init__(self,x_latitude,x_longitude,y_latitude,y_longitude,detailLevel):
        self.detailLevel = detailLevel
        self.left = Point(x_latitude,x_longitude,'nan')
        self.right = Point(y_latitude,y_longitude,'nan')
#         print(x_latitude,x_longitude,y_latitude,y_longitude)
        self.northWest = 0
        self.southWest = 0 
        self.southEast =0 
        self.northEast = 0
        self.pointList = ([])
        
    
    
    def __str__(self):
        return "Grid : %g , %g, \n %g %g" % (self.left.latitude,self.left.longitude,self.right.latitude,self.right.longitude)  
    __repr__ = __str__
    
    
    def getPoint(self,i,j):
        s = self.pointList
        for p in s:
            if(float_equal(p.latitude,i) and float_equal(p.longitude,j)):
                return p
        print("____________")
        print("POINT DOES NOT EXIST")
        print("____________")
 
        return Point(0.0,0.0)
    def setPointElevation(self,i,j,elev):
        
        self.getPoint(i,j).elevation = elev
    def contains(self,point):
        """Check if point is within bounds"""
        return (point.latitude < self.right.latitude 
                and point.latitude > self.left.latitude
                and point.longitude < self.right.longitude
                and point.longitude > self.left.longitude
                )
    def gridContains(self,point):
        """If grid has children - check them if contain given point, else - return if grid has point"""
        if(self.northWest and self.northWest.contains(point)) : 
            return self.northWest.gridContains(point)
        elif(self.southWest and self.southWest.contains(point)) : 
            return self.southWest.gridContains(point)
        elif(self.southEast and self.southEast.contains(point)) : 
            return self.southEast.gridContains(point)
        elif(self.northEast and self.northEast.contains(point)) : 
            return self.northEast.gridContains(point)
        else:
            if(self.contains(point)):
                return self
            else:
                return 0
    
    def toCurve(self,list = None):
        if list is None:
            list = []
        list.append( [ (self.left.latitude,self.left.longitude),(self.right.latitude,self.left.longitude),(self.right.latitude,self.right.longitude),(self.left.latitude,self.right.longitude),(self.detailLevel)])
        if(self.northWest!= 0):
            list.extend(self.northWest.toCurve())
        if(self.southWest):
            list.extend(self.southWest.toCurve())
        if(self.southEast):
            list.extend(self.southEast.toCurve())
        if(self.northEast):
            list.extend(self.northEast.toCurve())
        return list
    
    def deriveWithPath(self,path):
        rangeX = self.right.latitude - self.left.latitude
        rangeY = self.right.longitude - self.left.longitude
        
        for level in range(1,MAXLEVEL):
            for i in range(round(rangeX/(2*(2**(level+1)))),round(rangeX),round(rangeX/2**level)):
                for j in range(round(rangeY/(2*(2**(level+1)))),round(rangeY),round(rangeY/2**level)):
#                     print("i : %d j: %d"%(i,j))
                    p = Point(i,j)
#                     print(p)
                    found = self.gridContains(p)
                    local = path.pointDistance(p)
                    x = local[0]
                    y = local[1]
                    x1 = found.left.longitude
                    x2 = found.right.longitude
                    y1 = found.left.latitude
                    y2 = found.right.latitude
                    dist1 = dist(x1, y1, x1, y2,x, y)
                    dist2 = dist(x1, y1, x2, y1,x, y)
                    dist3 = dist(x1, y2, x2, y2,x, y)
                    dist4 = dist(x2, y1, x2, y2,x, y)
                    localDistance = min(dist1,dist2,dist3,dist4)
                    l = MAXLEVEL - int(math.log(calcSize(getLevel(localDistance,rangeX)),2))+1
                    if (found.detailLevel < l):
                        derive(found)
        self.pointList = self.getPoints()
    
    def getElevation(self,path="36.578581,-118.291994|36.23998,-116.83171"):
        
        http = urllib3.PoolManager()
        pointUrl = ''   
        points = self.pointList
        partedPoints = []
        i=0
        for p in points:
            if(len(pointUrl + '%g,%g|'%(p.latitude,p.longitude)) < 1500):
                pointUrl += '%g,%g|'%(p.latitude,p.longitude)
            else:
                partedPoints.append([pointUrl])
                pointUrl = ''
        partedPoints.append([pointUrl])
        for line in partedPoints:
            url = ELEVATION_BASE_URL + '?locations=' +  line[0][:-1] +"&key=" + KEY #urllib3.(elvtn_args)
            
            r = http.request_encode_url("GET", url)
            obj = simplejson.loads(r.data)
             
            sleep(0.3)
            for resultSet in obj['results']:
                i = float(resultSet['location']['lat'])
                j = float(resultSet['location']['lng'])
                elev = float(resultSet['elevation'])
                 
                self.setPointElevation(i,j,elev)
              
                self.writeToFile()
        return url
    def writeToFile(self):
        
        try:
            if(os.path.isfile(FILENAME)):
                open(FILENAME,'wb')
            new = open('tmp','wb')              
            pickle.dump(self,new)
            os.remove(FILENAME)
            new.close()
            os.rename('tmp',FILENAME)
            new= open(FILENAME,'rb')
            test = pickle.load(new)
        
        except pickle.PicklingError:
            print("Cound not save object to file")
        except pickle.UnpicklingError:
           print("Could not read object from file")
        except pickle.PickleError:
            print("Serialization error") 
        return (test.left == self.left and test.right == self.right and  test.detailLevel == self.detailLevel)
                          

    def getPoints(self,s = None):
        if s is None:
            s = []
       
        s.append(self.left)
        s.append(self.right)
        
        if(self.northWest):
            self.northWest.getPoints(s)
        if(self.southWest):
            self.southWest.getPoints(s)
        if(self.southEast):
            self.southEast.getPoints(s)
        if(self.northEast):
            self.northEast.getPoints(s)
        
        return set(s) 
def dist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = math.sqrt(dx*dx + dy*dy)

    return dist                    
                
                 
def getLevel(distance,size):
    return distance*64/size
                
def derive(grid):
    """Returns grid 
    ________________________________
    |               |               |
    |   northWest   |   northEast   | 
    |_______________|_______________| 
    |               |               | 
    |   southWest   |   southEast   |  
    |_______________|_______________|
    derived from the original grid
    """

    if(grid.detailLevel == MAXLEVEL): 
        return grid
    lx = float(grid.left.longitude)
    ly = float(grid.left.latitude)
    rx = float(grid.right.longitude)
    ry = float(grid.right.latitude)
    latmid = ((ly + ry) /2.0)
    longmid = ((lx + rx) /2.0)
    if(grid.northWest == 0) :
        grid.northWest = Grid(latmid,lx,ry,longmid,grid.detailLevel+1)
#         grid.northWest = derive(grid.northWest,level)
 
    else : 
        grid.northWest = derive(grid.northWest)
        
        
        
    if(grid.southWest == 0 ):
        grid.southWest = Grid(ly,lx,latmid,longmid,grid.detailLevel+1)
#         grid.southWest = derive(grid.southWest,level)
    
    else : 
        grid.southWest = derive(grid.southWest)
        
        
        
    if(grid.southEast == 0):
        grid.southEast = Grid(ly,longmid,latmid,rx,grid.detailLevel+1)
#         grid.southEast= derive(grid.southEast,level)

    else : 
        grid.southEast= derive(grid.southEast)
        
        
        
        
    if(grid.northEast == 0):
        grid.northEast = Grid(latmid,longmid,ry,rx,grid.detailLevel+1)
#         grid.northEast = derive(grid.northEast,level)
    else : 
        grid.northEast = derive(grid.northEast)
        
        
        
    return grid
    
