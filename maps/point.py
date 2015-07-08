class Point:
    longitude = 0.0
    latitude = 0.0
    timestamp = 0
    def __init__(self,longitude,latitude,timestamp='nan'):
        self.longitude = longitude
        self.latitude = latitude
        self.timestamp = timestamp
    def __str__(self):
        return "Point(%f,%f,%s)"%(self.longitude,self.latitude,self.timestamp)
    __repr__ = __str__
    