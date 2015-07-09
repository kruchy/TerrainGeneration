from point import Point
from gi.overrides.keysyms import Right
class Grid:
    detailLevel = 0
    
    #coordinates
    #south west corner
    left = Point(0,0)
    #north east corner
    right = Point(0,0)
    
    #children grids
    (northWest,southWest,southEast,northEast) = (0,0,0,0) 
    
    def __init__(self,x_latitude,x_longitude,y_latitude,y_longitude,detailLevel):
        self.detailLevel = detailLevel
        self.left = Point(x_latitude,x_longitude,'nan')
        self.right = Point(y_latitude,y_longitude,'nan')
        
    
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
        return 0
    latmid = (grid.left.latitude + grid.right.latitude /2)
    longmid = (grid.left.longitude + grid.right.longitude /2)
    return(
           Grid(latmid,grid.left.longitude,grid.right.latitude,longmid,grid.detailLevel+1),
           Grid(grid.left.latitude,grid.left.longitude,latmid,longmid,grid.detailLevel+1),
           Grid(latmid,longmid,grid.right.latitude,grid.right.longitude,grid.detailLevel+1),
           Grid(grid.left.latitude,longmid,latmid,grid.right.longitude,grid.detailLevel+1)
           )
    
    