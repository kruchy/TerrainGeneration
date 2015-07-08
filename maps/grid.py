from point import Point
class Grid:
    detailLevel = 0
    
    #coordinates
    left = Point(0,0)
    right = Point(0,0)
    
    #children grids
    (lt,lb,rb,rt) = (0,0,0,0)
    
    
    def __init__(self,detailLevel):
        self.detailLevel = detailLevel
        
    def derive(self):
        pass
    
    