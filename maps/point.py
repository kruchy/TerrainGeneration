import math
from utils import float_equal
class Point(object):
    EARTH_RADIUS= 6371
    longitude = 0.0
    latitude = 0.0
    elevation = 0.0
    timestamp = 0
    def __init__(self,latitude,longitude,elevation=0.0,timestamp='nan'):
        self.latitude = latitude
        
        self.longitude = longitude
        self.timestamp = timestamp
        self.elevation = 0.0
    def __str__(self):
        return "Point(%f,%f,%f,%s)"%(self.latitude,self.longitude,self.elevation,self.timestamp)
    __repr__ = __str__
    
    def __eq__(self,other):
        return ( float_equal(self.latitude,other.latitude) and
                float_equal(self.longitude,other.longitude) and
                float_equal(self.elevation,other.elevation) and
                self.timestamp == other.timestamp)
    
    def __hash__(self):
        return hash(self.__repr__())    
    #distance between 2 points on map
def distance(p1,p2):
    dLat =  math.radians(p2.latitude - p1.latitude)
    dLong = math.radians(p2.longitude-p1.longitude)
    a = math.sin(dLat/2)*math.sin(dLat/2) + math.cos(math.radians(p1.latitude)) * math.cos(math.radians(p2.latitude)) * math.sin(dLong/2)*math.sin(dLong/2)
    c = 2* math.atan2(math.sqrt(a), math.sqrt(1-a))
    return Point.EARTH_RADIUS * c * 1000
    
         