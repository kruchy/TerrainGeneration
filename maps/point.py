import math
class Point:
    EARTH_RADIUS= 6371
    longitude = 0.0
    latitude = 0.0
    timestamp = 0
    def __init__(self,latitude,longitude,timestamp='nan'):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
    def __str__(self):
        return "Point(%f,%f,%s)"%(self.latitude,self.longitude,self.timestamp)
    __repr__ = __str__
    
    #distance between 2 points on map
def distance(p1,p2):
    dLat = math.radians(p2.latitude - p1.latitude)
    dLong = math.radians(p2.longitude-p1.longitude)
    a = math.sin(dLat/2)*math.sin(dLat/2) + math.cos(math.radians(p1.latitude)) * math.cos(math.radians(p2.latitude)) * math.sin(dLong/2)*math.sin(dLong/2)
    c = 2* math.atan2(math.sqrt(a), math.sqrt(1-a))
    return Point.EARTH_RADIUS * c * 1000
    
         