import point
from point import distance
import math
class Path(object):
    pointList = []
    def __init__(self):
        self.pointList = []
    
    def __repr__(self):

        s ="Path : %d point%s" % (len(self.pointList),'s'*(len(self.pointList)!=1))
        return s
        
    def __str__(self):
        s = "Path : "
        for x in self.pointList:
            s + str(x)
            print(x)
        return s
    
    def getPointsFromFile(self,filename):
        with open(filename,'r') as f:
            for line in f.readlines():
                l = line.split(',')
                self.addPoint(point.Point(float(l[1]),float(l[0])))
    
    def addPoint(self,point):
        self.pointList.append(point)
        
    def removePoint(self,point):
        self.pointList.remove(point)
        

    def maxDistance(self):
        """
        might be useful someday
        """
        max = 0
        for i in range(0,len(self.pointList)-2):
            for j in range(i,len(self.pointList)-1):
                dist =distance(self.getAt(i),self.getAt(j)) 
                if(dist > max):
                    max = dist
        return max
                
    def getAt(self,i):
        if(i<len(self.pointList)):
            return self.pointList[i]
        else:
            return 0
    
    def pointDistance(self,point):
        
        """
        |y2-y1           x2y1 - x1y2|
        |x2-x1 * x - y +   x2-x1    |
        -----------------------------
           /      2
          /y2 - y1 
        \/ x2 - x1    + 1
        distance between point and path section
        """
        
        min = 10000
        x = 0.0
        y = 0.0
        for p in self.pointList:
#             p1 = self.getAt(i)
#             p2 = self.getAt(i+1)
#             deltaLat=   p2.latitude - p1.latitude
#             deltaLong = p2.longitude - p1.longitude
#             dist = math.fabs(point.longitude * (deltaLat/deltaLong) - point.latitude + ( (p2.longitude * p1.latitude) - (p1.longitude*p2.latitude))/deltaLong)/math.sqrt(math.pow(deltaLat/deltaLong,2) + 1)
#             print(p.latitude)
#             print(point.latitude)
#             print(p.longitude)
#             print(point.longitude)
#             print("----------------")
            dist = math.fabs(p.latitude - point.latitude) + math.fabs(p.longitude- point.longitude)
#             print(dist,p.latitude,p.longitude,point.latitude,point.longitude)
            if (dist < min):
                min = dist
                x = p.longitude
                y = p.latitude
        return x,y,dist
    def getMaxLat(self):
        lat = -90
        for p in self.pointList:
            if p.latitude > lat:
                lat = p.latitude
        return lat
    def getMaxLng(self):
        lng = -180
        for p in self.pointList:
            if p.longitude > lng:
                lng = p.longitude
        return lng
    def getMinLat(self):
        lat = 90
        for p in self.pointList:
            if p.latitude < lat:
                lat = p.latitude
        return lat
    def getMinLng(self):
        lng = 180
        for p in self.pointList:
            if p.longitude < lng:
                lng = p.longitude
        return lng
    
        
