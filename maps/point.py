class Point:
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
    