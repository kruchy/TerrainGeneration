from xml import etree
import math
epsilon = 0.00001
METER = 111111.0
EARTH_RADIUS= 6371
def calcSize(number):
    power = 1
    while(power < number):
        power = power*2
    return power
def resultsFromJson(str):
    if str['status'] == 'OK':
        return str['results']
def float_equal(a,b):
    return math.fabs(a - b) <= epsilon



def calculateRange(val,min,max,newMin,newMax):
    return (val-min)/(max-min)*(newMax - newMin) + newMin
    

def gridDistance(grid,point):
    x1 = grid.leftDown.longitude
    x2 = grid.rightUp.longitude
    y1 = grid.leftDown.latitude
    y2 = grid.rightUp.latitude
    x = point.longitude
    y = point.latitude
    dist1= dist(x1,y1,x2,y1,x,y)
    dist2 = dist(x1,y1,x1,y2,x,y)
    dist3 = dist(x2,y1,x2,y2,x,y)
    dist4 = dist(x1,y2,x2,y2,x,y)
    return(min(dist1,dist2,dist3,dist4))

    
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

def pointDistance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

def googleToX(lat,lng):
    x = EARTH_RADIUS * math.cos(lat) * math.cos(lng)
    y = EARTH_RADIUS * math.cos(lat) * math.sin(lng)          
    return math.fabs(y),math.fabs(x)
def chunks(l,n):
    n = max(1,n)
    return [l[i:i+1] for i in xrange(0,len(l),n)]