from point import Point
import utils
import math
import pickle
import urllib3
import datetime
import os
import glob
import simplejson
import numpy
from time import sleep
from utils import float_equal, calcSize, gridDistance

KEY = 'AIzaSyD4YJdwmlO6sIyJ94egzfy3TLfaai4faAY'
ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
FILENAME = '2708'
METER = 1/11111.0

class Grid(object):
    detailLevel = 0
    #coordinates
    #south west corner
    leftDown = Point(0,0)
    #north east corner
    leftUp = Point(0,0)
    rightDown = Point(0,0)
    rightUp = Point(0,0)
    pointList = set([])
    biggestChild = 0
    #children grids
    northWest,southWest,southEast,northEast = 0,0,0,0
    
    
    def __init__(self,x_latitude,x_longitude,y_latitude,y_longitude,detailLevel):
        self.detailLevel = detailLevel
        self.leftDown = Point(x_latitude,x_longitude,'nan')
        self.rightUp = Point(y_latitude,y_longitude,'nan')
        self.leftUp = Point(y_latitude,x_longitude,'nan')
        self.rightDown = Point(x_latitude,y_longitude,'nan')
        
        self.northWest = 0
        self.southWest = 0 
        self.southEast = 0 
        self.northEast = 0
        self.biggestChild = 0
        self.pointList = ([])
        
    
    
    
    def __str__(self):
        return "Grid : %g , %g, \n %g %g" % (self.leftDown.latitude,self.leftDown.longitude,self.rightUp.latitude,self.rightUp.longitude)  
    __repr__ = __str__
    
    
    def getPoint(self,i,j):
        for p in [self.leftUp,self.leftDown,self.rightDown,self.rightUp]:
#             print(p,i,j)
            
            if(float_equal(p.latitude,i) and float_equal(p.longitude,j)):
                
#                 with open('el.txt','a') as f:
#                     f.write('%f %f, %f %f'%(p.latitude,i,p.longitude,j)+ os.linesep)
                return p
        
        else:
            latmid = (self.leftDown.latitude + self.rightUp.latitude) /2
            lngmid = (self.leftDown.longitude + self.rightUp.longitude) /2
#             print(i,latmid,j,lngmid)
            if(self.northWest and i > latmid and j < lngmid ) :
                p =  self.northWest.getPoint(i,j)
                if(p):
                    return p
            if( self.northEast and i > latmid and j > lngmid ) :
                p =  self.northEast.getPoint(i,j)
                if(p):
                    return p
            if( self.southEast and i < latmid and j > lngmid ) :
                p =  self.southEast.getPoint(i,j)
                if(p):
                    return p
            if( self.southWest and i < latmid and j < lngmid ):
                p =  self.southWest.getPoint(i,j)
                if(p):
                    return p
#         print(i,j,latmid,lngmid)
        return False
    def setPointElevation(self,i,j,elev):
        p =self.getPoint(i,j)
    
        if(p): 
            p.elevation = elev
    def contains(self,point):
        return (point.latitude < self.rightUp.latitude 
                and point.latitude > self.leftDown.latitude
                and point.longitude < self.rightUp.longitude
                and point.longitude > self.leftDown.longitude
                )
    def gridContains(self,point):
        
        if(self.northWest and self.northWest.contains(point)) : 
            return self.northWest.gridContains(point)
        elif(self.southWest and self.southWest.contains(point)) : 
            return self.southWest.gridContains(point)
        elif(self.southEast and self.southEast.contains(point)) : 
            return self.southEast.gridContains(point)
        elif(self.northEast and self.northEast.contains(point)) : 
            return self.northEast.gridContains(point)
        else:
            if(self.contains(point)):
                return self
            else:
                return 0
    
    def toCurve(self,list = None):
        if list is None:
            list = []
        list.append( [ (self.leftDown.latitude,self.leftDown.longitude),(self.leftUp.latitude,self.leftUp.longitude),(self.rightUp.latitude,self.rightUp.longitude),(self.rightDown.latitude,self.rightDown.longitude)])
        if(self.northWest):
            list.extend(self.northWest.toCurve())
        if(self.southWest):
            list.extend(self.southWest.toCurve())
        if(self.southEast):
            list.extend(self.southEast.toCurve())
        if(self.northEast):
            list.extend(self.northEast.toCurve())
        return list
    
    def deriveWithPath(self,path):
        for p in path.pointList:
            print(p)
            derive(self,p)

    def updateElevationFromFile(self,filename):
        with open(filename,'r') as f:
            lines = f.readlines()
            size = len(lines)
            print('Lines to read: %d'%size)
            percent = -1.0
            count = 0
            for line in lines:
                count+=1
                if(percent != round(float(count* 100)/size )):
                    percent = round(float(count* 100)/size )
                    print(percent)
                s = line.split(',')
                lat = float(s[0])
                lng = float(s[1])
                elev = float(s[2])
                self.setPointElevation(lat, lng, elev)


    def getElevation(self):
        
        http = urllib3.PoolManager()
        pointUrl = ''   
        points = self.pointList
        partedPoints = []
        i=0
        baseUrl =ELEVATION_BASE_URL + '?locations=' +"&key=" + KEY
        for p in points:
            if(len(pointUrl + '%g,%g|'%(p.latitude,p.longitude)) + len(baseUrl)< 2000):
                pointUrl += '%g,%g|'%(p.latitude,p.longitude)
            else:
                partedPoints.append([pointUrl])
                pointUrl = ''
        partedPoints.append([pointUrl])
        for line in partedPoints:
            url = ELEVATION_BASE_URL + '?locations=' +  line[0][:-1] +"&key=" + KEY #urllib3.(elvtn_args)
            
            r = http.request_encode_url("GET", url)
            obj = simplejson.loads(r.data)
            
            sleep(0.21)
            for resultSet in obj['results']:
                i = float(resultSet['location']['lat'])
                j = float(resultSet['location']['lng'])
                elev = float(resultSet['elevation'])
              
                self.setPointElevation(i,j,elev)
                p = self.getPoint(i, j)
                with open('backup.txt','a') as f:
                    f.write("%g,%g,%g"%(p.latitude,p.longitude,p.elevation))
                self.writeToFile()
        return url
    def writeToFile(self,filename):
        
        try:
            if(os.path.isfile(filename)):
                print('Overwriting file ' + filename)
            print('Saving grid to file ' + filename)
            new = open(filename,'wb') 
            pickle.dump(self,new,2)
            print('Saved to file ' + filename)
            new.close()
            print("written")
        
        except pickle.PicklingError:
            print("Cound not save object to file")
        except pickle.UnpicklingError:
           print("Could not read object from file")
        except pickle.PickleError:
            print("Serialization error") 
        
    def pointsToChunks(self):
        s = [p for item in self.toCurve() for p in item]
        s = set(s)
        size = len(s)
        i=0
        for p in s:
            print(float(i)/size * 100)
            i+=1
            list.append(p)
        chunkNum = int(math.ceil(float(len(s))/1280000))
        chunkSize  = len(list)/chunkNum
        partList = []
        print("Points %d"%len(list))
        print("Chunk Size %d"%chunkSize)
        print("Chunk Num %d" %chunkNum)
        print("dumping")             
        for i in range(chunkNum):
            with open('chunkList%d'%i,'wb') as f:
                print(len(list[i*chunkSize:(i+1)*chunkSize+1]))
                partList.append(list[i*chunkSize:(i+1)*chunkSize+1])
                pickle.dump(list[i*chunkSize:(i+1)*chunkSize+1],f,2)
                print("dumped %d"%i) 
    
    def rangeElevation(self):
        min = 999999999999999
        max = -9999999999999999
    
        data = self.get()
        for p in data:
            if(p.elevation > max):
                max = p.elevation
            if(p.elevation < min) : 
                min = p.elevation
        return min,max               
    def get(self):
        res = set(self.getPoints())
        print(len(res))
        return res
    def getPoints(self,s = None):
        if s is None:
            s = []
        s.append(self.leftUp)
        s.append(self.rightUp)
        s.append(self.leftDown)
        s.append(self.rightDown)
        
        if(self.northWest):
            self.northWest.getPoints(s)
        if(self.southWest):
            self.southWest.getPoints(s)
        if(self.southEast):
            self.southEast.getPoints(s)
        if(self.northEast):
            self.northEast.getPoints(s)
        
        return s 
    
    def countGrids(self,c=None):
        if c is None:
            c= 0
        if(self.northWest):
            c += self.northWest.countGrids()
        if(self.southWest):
            c += self.southWest.countGrids()
        if(self.southEast):
            c += self.southEast.countGrids()
        if(self.northEast):
            c += self.northEast.countGrids()
        return c+1  
        
 
                
def derive(grid,point,once=False):
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
    if(grid.detailLevel == 1): 
        return grid
    
    distance = gridDistance(grid,point)
    list = []
#     list.append(grid.left)
#     list.append(grid.right)
#     list.append(Point(grid.left.latitude,grid.right.longitude))
#     list.append(Point(grid.right.latitude,grid.left.longitude))
    lx = float(grid.leftDown.longitude)
    ly = float(grid.leftDown.latitude)
    rx = float(grid.rightUp.longitude)
    ry = float(grid.rightUp.latitude)
    latmid = ((ly + ry) /2.0)
    longmid = ((lx + rx) /2.0)
#     list.append(Point(latmid,longmid))

    if(grid.northWest == 0):
        grid.northWest = Grid(latmid,lx,ry,longmid,grid.detailLevel/2)
        grid.northWest.leftUp = grid.leftUp
    if(not once and  doDerive(gridDistance(grid.northWest,point),grid.northWest) ):
        derive(grid.northWest, point)
        
        
        
    if(grid.southWest == 0):
        grid.southWest = Grid(ly,lx,latmid,longmid,grid.detailLevel/2)
        grid.southWest.leftDown = grid.leftDown
    if(not once and  doDerive(gridDistance(grid.southWest,point),grid.southWest)):
        derive(grid.southWest, point)
        
    if(grid.southEast == 0):
        grid.southEast = Grid(ly,longmid,latmid,rx,grid.detailLevel/2)
        grid.southEast.rightDown = grid.rightDown
    if(not once and  doDerive(gridDistance(grid.southEast,point),grid.southEast)):
        derive(grid.southEast,point)

        
        
        
    if(grid.northEast == 0):    
        grid.northEast.rightUp = grid.rightUp
        grid.northEast = Grid(latmid,longmid,ry,rx,grid.detailLevel/2)
    if(not once and  doDerive(gridDistance(grid.northEast,point),grid.northEast) ):
        derive(grid.northEast, point)
    
        
    return grid

def readFromFile(filename):
    if(not os.path.isfile(filename)):
        raise IOError('File %s does not exist'%filename)
    with open(filename,'rb') as f:
        res = pickle.load(f)
    print('Loaded ' + filename)
    res.pointList = res.get()
    return res
    
           
def doDerive(distance,grid):
    x = math.log(grid.detailLevel,2)
    return( 
#             distance <  1100*METER and x >5 or
#             distance <  600*METER and x > 4 or
#             distance <  300*METER  and x > 3 or
#             distance <  100*METER and x > 2 or
#             distance <  50*METER   and x > 1 or
#             distance <  25*METER   and x > 0 or
#             distance <  100*METER)
#             distance < 2100 and x > 6 or
#             distance <  1100*METER and x >5 or
#             distance <  600*METER and x > 4 or
#             distance <  300*METER  and x > 3 or
            distance <  2100*METER and x > 2 or
            distance <  400*METER   and x > 1 or
            distance <  80*METER   and x > 0 )#             distance <  100*METER)

def rangeElevationFromFile(filename):
    min = 999999999999999
    max = -9999999999999999
    with open(filename,'r') as f:
        data = f.readlines()
        for line in data:
            s = line.strip().split(',')
            tmp = float(s[2])
            if(tmp > max):
                max = tmp
            if(tmp < min) : 
                min = tmp
    return min,max

def heightmapFromGrid(grid,heightMapSize):
    count = 0
    minx,miny,maxx,maxy = grid.leftDown.longitude,grid.leftDown.latitude,grid.rightUp.longitude,grid.rightUp.latitude
    percent = -1.0
    minElev,maxElev = grid.rangeElevation()
    if(float_equal(minElev,maxElev)):
        maxElev +=1
    x = numpy.zeros((heightMapSize,heightMapSize))
    rangey = numpy.linspace(miny,maxy,num=heightMapSize,endpoint=False)
    rangex = numpy.linspace(minx,maxx,num = heightMapSize,endpoint= False)
    for i in xrange(2,heightMapSize):
        for j in xrange(2,heightMapSize):
            count +=1
            if(percent != round(float(count*100)/((heightMapSize-2)**2) )):
                percent = round(float(count*100)/((heightMapSize-2)**2) )
                print(percent)
            p = Point(rangey[i],rangex[j])
            tmp = grid.gridContains(p)
            dist1 = utils.pointDistance(p.longitude,p.latitude,tmp.leftDown.longitude,tmp.leftDown.latitude)
            dist2 = utils.pointDistance(p.longitude,p.latitude,tmp.leftUp.longitude,tmp.leftUp.latitude)
            dist3 = utils.pointDistance(p.longitude,p.latitude,tmp.rightDown.longitude,tmp.rightDown.latitude)
            dist4 = utils.pointDistance(p.longitude,p.latitude,tmp.rightUp.longitude,tmp.rightUp.latitude)
            elev = (dist1*tmp.leftDown.elevation + dist2*tmp.leftUp.elevation + dist3*tmp.rightDown.elevation + dist4*tmp.rightUp.elevation)/(dist1+dist2+dist3+dist4)
            x[i-1,j-1] = ((elev - minElev )/ (maxElev  - minElev))
    return x
def readFromFiles():
    for i in ['southEast','southWest','northEast','northWest']:
        if(not os.path.isfile(i)):
            raise IOError('File %s does not exist'%i)
        for j in range(1,5):
            if(not os.path.isfile('%d'%j + i)):
                print('File %s does not exist'%(str(j)+i))
                raise IOError('File %s does not exist'%(str(j)+i))
    with open('mainGrid','rb') as f:
        grid = pickle.load(f)
    with open('southEast','rb') as f:
        grid.southEast = pickle.load(f)
        print('SouthEast loaded')
    with open('southWest','rb') as f:
        grid.southWest = pickle.load(f)
        print('SouthWest loaded')
    with open('northEast','rb') as f:
        grid.northEast = pickle.load(f)
        print('NorthEast loaded')
    with open('northWest','rb') as f:
        grid.northWest = pickle.load(f)
        print('NorthWest loaded')
    i = 0
    for g in [grid.southEast,grid.southWest,grid.northEast,grid.northWest]:
        j = 1
        i+=1
        with open('%dsouthEast'%i,'rb') as f:
            g.southEast = pickle.load(f)
        print('Child %d %d%% loaded'%(i,float(j)/4*100))
        j+=1
        with open('%dsouthWest'%i,'rb') as f:
            g.southWest = pickle.load(f)
        print('Child %d %d%% loaded'%(i,float(j)/4*100))
        j+=1
        with open('%dnorthEast'%i,'rb') as f:
            g.northEast = pickle.load(f)
        print('Child %d %d%% loaded'%(i,float(j)/4*100))
        j+=1
        with open('%dnorthWest'%i,'rb') as f:
            g.northWest = pickle.load(f) 
        print('Child %d %d%% loaded'%(i,float(j)/4*100))
    print('Loaded grid')
    grid.pointList = grid.get()
    return grid

def gridFromPath(path):
    maxLng  = path.getMaxLng()
    maxLat  = path.getMaxLat()
    minLng  = path.getMinLng()
    minLat  = path.getMinLat()
    m = max(maxLng- minLng,maxLat - minLat)
    m = m+0.04
    m = utils.METER * m
    m = calcSize(m)
    diff = m*(1/utils.METER)
    grid = Grid(minLat,minLng,minLat + diff,minLng + diff,m )
    return grid
    
def deriveAndSave(grid,path):
    
    size = len(path.pointList)
    with open('mainGrid','wb') as f:
        pickle.dump(grid, f, 2)
    with open('southEast','wb') as f:
        pickle.dump(grid.southEast,f,2)
    with open('southWest','wb') as f:
        pickle.dump(grid.southWest,f,2)
    with open('northEast','wb') as f:
        pickle.dump(grid.northEast,f,2)
    with open('northWest','wb') as f:
        pickle.dump(grid.northWest,f,2)
    grid = None
    j = 0
    filenames = ['southEast','southWest','northEast','northWest']
    for name in filenames:
         
        j +=1
        with open(name,'rb') as f:
            grid = pickle.load(f)
        print("LOADED " + name)
        derive(grid,Point((grid.rightUp.latitude - grid.leftDown.latitude)/2.0,(grid.rightUp.longitude - grid.leftDown.longitude)/2.0),True)
        with open('%dsouthEast'%j,'wb') as f:
            pickle.dump(grid.southEast,f,2)
        with open('%dsouthWest'%j,'wb') as f:
            pickle.dump(grid.southWest,f,2)
        with open('%dnorthEast'%j,'wb') as f:
            pickle.dump(grid.northEast,f,2)
        with open('%dnorthWest'%j,'wb') as f:
            pickle.dump(grid.northWest,f,2)
        grid = None
        for childName in filenames:
            with open('%d'%j+childName,'rb') as f:
                grid = pickle.load(f)
            i = 0
            for p in path.pointList:
                i+=1
                print('Child : ' + str(j) + ' '+ str(float(i)/size *100))
                derive(grid,p)
            with open('%d'%j+childName,'wb') as f:
                pickle.dump(grid,f,2)
            grid = None
        with open(name,'wb') as f:
            grid = pickle.dump(grid,f,2)
        print('dumped')
        
        
