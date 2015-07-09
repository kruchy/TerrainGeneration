from point import Point
class Grid:
    detailLevel = 0
    
    #coordinates
    #south west corner
    left = Point(0,0)
    #north east corner
    right = Point(0,0)
    
    #children grids
    northWest,southWest,southEast,northEast = 0,0,0,0
    children = (northWest,southWest,southEast,northEast) 
    
    def __init__(self,x_latitude,x_longitude,y_latitude,y_longitude,detailLevel):
        self.detailLevel = detailLevel
        self.left = Point(x_latitude,x_longitude,'nan')
        self.right = Point(y_latitude,y_longitude,'nan')
        self.northWest = 0
        self.southWest = 0 
        self.southEast =0 
        self.northEast = 0
        
    
    def __str__(self):
        return "Grid : %d , %d, \n %d %d" % (self.left.latitude,self.left.longitude,self.right.latitude,self.right.longitude)  
    
    def contains(self,point):
        return (point.latitude < self.right.latitude 
                and point.latitude > self.left.latitude
                and point.longitude < self.right.longitude
                and point.longitude > self.left.longitude
                )
    def gridContains(self,point):
        if(self.northWest and self.northWest.contains(point)) : 
            return self.northWest
        elif(self.southWest and self.southWest.contains(point)) : 
            return self.southWest
        elif(self.southEast and self.southEast.contains(point)) : 
            return self.southEast
        elif(self.southEast and self.northEast.contains(point)) : 
            return self.northEast
        else:
            if(self.contains(point)):
                return self
            else:
                return 0
    
    def toCurve(self,list = None):
        if list is None:
            list = []
        list.append( [(self.left.latitude,self.left.longitude),(self.right.latitude,self.left.longitude),(self.right.latitude,self.right.longitude),(self.left.latitude,self.right.longitude),(self.detailLevel)])
        if(self.northWest!= 0):
            list.extend(self.northWest.toCurve())
        if(self.southWest):
            list.extend(self.southWest.toCurve())
        if(self.southEast):
            list.extend(self.southEast.toCurve())
        if(self.northEast):
            list.extend(self.northEast.toCurve())
        return list
    __repr__ = __str__
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

    if(grid.detailLevel == 6): 
        return grid
    latmid = (grid.left.latitude + grid.right.latitude /2)
    longmid = (grid.left.longitude + grid.right.longitude /2)
    if(grid.northWest == 0) :
        grid.northWest = Grid(latmid,grid.left.longitude,grid.right.latitude,longmid,grid.detailLevel+1)
    else : 
        derive(grid.northWest)
    if(grid.southWest == 0 ):
        grid.southWest = Grid(grid.left.latitude,grid.left.longitude,latmid,longmid,grid.detailLevel+1)
    else : 
        derive(grid.southWest)
    if(grid.southEast == 0):
        grid.southEast = Grid(latmid,longmid,grid.right.latitude,grid.right.longitude,grid.detailLevel+1)
    else : 
        derive(grid.southEast)
    if(grid.northEast == 0):
        grid.northEast = Grid(grid.left.latitude,longmid,latmid,grid.right.longitude,grid.detailLevel+1)
    else : 
        derive(grid.northEast)
    return grid
    


             
    