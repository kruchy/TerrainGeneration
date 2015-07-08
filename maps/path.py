class Path:
    pointList = []
    def __init__(self):
        pointList = []
    
    def __repr__(self):

        s ="Path : %d point%s" % (len(self.pointList),'s'*(len(self.pointList)!=1))
        return s
        
    def __str__(self):
        s = "Path : "
        for x in self.pointList:
            s + str(x)
        return s
    
    def addPoint(self,point):
        self.pointList.append(point)
        
    def removePoint(self,point):
        self.pointList.remove(point)
        
    