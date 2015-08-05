from sets import Set
import cPickle as pickle
import maps.point as points
from maps.path import *
from maps.grid import *
from operator import attrgetter 
import io
import urllib3
import json
from grid import calcSize, readFromFile, derive, METER
import utils
import datetime
import numpy
import xml.etree.ElementTree as ET
from utils import calculateRange
import simplejson
from time import sleep


KEY = 'AIzaSyBPgO_hEbeiOuUvqmbgrpUoBUOr1nM4P9s'
ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
root = 'C:\\Terraingeneration\\23_07_2015\\'
folders = ['GRAPH_01','GRAPH_02','PROGOS_01','PROGOS_02']
fileName = 'resultTest'
if __name__ == '__main__':

#     grid = readFromFiles()
#     grid = readFromFile('2southWest')
#     grid.southWest = readFromFile('southWest')
#     grid.southEast = readFromFile('southEast')
#     grid.northWest= readFromFile('northWest')
#     grid.northEast = readFromFile('northEast')
#     print(grid.leftDown,grid.rightUp)
#     latmid = (grid.leftDown.latitude + grid.rightUp.latitude) /2
#     lngmid = (grid.leftDown.longitude + grid.rightUp.longitude) /2
#     print(latmid,lngmid)
#     print(grid.southWest) 
#     print(grid.southEast) 
#     print(grid.northWest) 
#     print(grid.northEast) 
    
        
# #     with open('elevations.txt','w') as f:
# #         for p in grid.getPoints():
# #             f.write('%f,%f,%f'%(p.latitude,p.longitude,p.elevation) + os.linesep)

#     grid.updateElevationFromFile('FINALRESULT.txt')
#     grid.writeToFile('updatedGrid')
#     print('UPDATED ELEVATION')
#     x = heightmapFromGrid(grid, 1000)
#     print('done heightmap')
#     print(x)
# #     with open('heightMap','wb') as f:
# #         pickle.dump(x,f)
# #     print('dumped heightmap')
#     with open('elevationsFinal.txt','w') as f:
#         rangex,rangey = x.shape
#         for i in xrange(rangex):
#             for j in xrange(rangey):
#                 f.write('%f,%f,%f'%(i,j,x[i,j])+ os.linesep)
    
#     list = []
#     minLat = 99999999999
#     maxLat = -9999999999
#     minLng= 99999999999
#     maxLng = -9999999999
#      
#     with open('FINALRESULT.txt','r') as f:
#         lines = f.readlines()
#         for line in lines:
#             p = line.strip().split(',')
#             y,x,z =float(p[0]),float(p[1]),float(p[2])
#             if(y > maxLat):
#                 maxLat = y
#             if(x > maxLng):
#                 maxLng = x
#             if(y < minLat):
#                 minLat = y 
#             if(x < minLng):
#                 minLng = x
#             list.append((y,x,z))
#     print(minLat,maxLat,minLng,maxLng)
#     size = int(math.ceil(math.sqrt(len(list))))
#     size = 1000
#     print(size)
#     first = numpy.zeros((size,size))
#     for p in list:
#         x = calculateRange(p[0],minLat,maxLat,0, size-1)
#         y = calculateRange(p[1],minLng,maxLng,0, size-1)
#         first[x,y]= p[2]
#     print(first)
# #     with open('firstTable','wb') as f:
# #         pickle.dump(first, f, 2)
#     count = 0
#     percent = -1.0
#     with open('firstTabletxt.txt','w') as f:
#         for i in xrange(size):
#             for j in xrange(size):
#                 count +=1
#                 if(percent != round(float(count*100)/size**2)):
#                     percent = round(float(count*100)/size**2)
#                     print(percent)
#                 f.write('%d,%d,%f'%(i,j,first[i,j])+ os.linesep)

#     
    
    
#     WCZYTANIE SCIEZKI
#     with open('lineCoords.txt') as f:
#         for line in f.readlines()[1:-1]:
#             l = line.split(',')
#             path.addPoint(points.Point(float(l[1]),float(l[0])))
#     maxLng  = path.getMaxLng()
#     maxLat  = path.getMaxLat()
#     minLng  = path.getMinLng()
#     minLat  = path.getMinLat()
#     m = max(maxLng- minLng,maxLat - minLat)
#     m = m+0.04
#     m = utils.METER * m
#     m = calcSize(m)
#     diff = m*(1/utils.METER)
#     viewPath = Path()
#     p1 = 0
#     p2 = 0
#     print(diff)
#     print(diff * utils.METER)
#     print(m)
#     TWORZENIE GRIDA NA PODSTAWIE SCIEZKI
#     grid = Grid(minLat-0.06,minLng-0.06,minLat - 0.06 + diff,minLng -0.06 + diff,m/8 )
#     print(grid.leftDown)
#     print(grid.rightUp)
#     print((grid.rightUp.latitude - grid.leftDown.latitude)*utils.METER , (grid.rightUp.longitude - grid.leftDown.longitude) * utils.METER)
#     s = [p for item in grid.toCurve() for p in item]
#     s = Set(s)
#     size = len(s)
#     print(size)
#     size = len(path.pointList)
#     j = 0
#     derive(grid,points.Point((grid.rightUp.latitude - grid.leftDown.latitude)/2.0,(grid.rightUp.longitude - grid.leftDown.longitude)/2.0),True)
#     s = [p for item in grid.toCurve() for p in item]
#     s = Set(s)




#    DZIELENIE GRIDA I ZAPISYWANIE DO PLIKU

#     

# odczytywanie z pliku
 
#     grid = readFromFiles()
#     with open('finalGrid','wb') as f:
#         pickle.dump(grid,f,2)
#     grid.writeToFile('test')
    
#     s = [p for item in grid.toCurve() for p in item]
#     s = Set(s)
#     i = 0
#     size = len(s)
#     print(size)
#     with open('pickledGrid.txt','w') as f:
#         for p in s:
#             i+=1
#             print(float(i)/size * 100)
#             f.write('%f,%f'%(p[0]*1000000,p[1]*1000000) + os.linesep)
#     print('Done\n')
#     print("Grid size = %d"%size)
#     
#     list = []
#     s = [p for item in grid.toCurve() for p in item]
#     s = Set(s)
#     size = len(s)
#     i=0
#     for p in s:
#         print(float(i)/size * 100)
#         i+=1
#         list.append(p)
#     chunkNum = int(math.ceil(float(len(s))/1280000))
#     chunkSize  = len(list)/chunkNum
#     partList = []
#     print("Points %d"%len(list))
#     print("Chunk Size %d"%chunkSize)
#     print("Chunk Num %d" %chunkNum)
#     print("dumping")             
#     for i in range(chunkNum):
#         with open('backuplist%d'%i,'wb') as f:
#             print(len(list[i*chunkSize:(i+1)*chunkSize+1]))
#             partList.append(list[i*chunkSize:(i+1)*chunkSize+1])
#             pickle.dump(list[i*chunkSize:(i+1)*chunkSize+1],f,2)
#             print("dumped %d"%i)         
#     partList = []
#     for i in range(2):
#         with open('backuplist%d'%i,'rb') as f:
#             print('Load %d'%i)
#                
#             tmp = pickle.load(f)
#             print('Tmp size %d'%len(tmp))
#             partList.extend(tmp)
#               
#     size = len(partList)
#     pointUrl = ''   
#     partedPoints = []
#     urlList = []
#     baseUrl =ELEVATION_BASE_URL + '?locations=' +"&key=" + KEY 
#     maxPoints = 0
#     i = 0
#     for p in partList:
#         maxPoints += 0
#         if(len(pointUrl + '%.7f,%.7f|'%(float(p[0])/1000000,float(p[1])/1000000)) + len(baseUrl)< 2000):
#             pointUrl += '%.7f,%.7f|'%(float(p[0]),float(p[1]))
#             maxPoints +=1
#             i+=1
#             if(maxPoints >=512):
#                 print('Max points exceeded %d'%maxPoints)
#         else:
#             partedPoints.append(pointUrl)
#             pointUrl = ''
#             maxPoints = 1
#             pointUrl += '%.7f,%.7f|'%(float(p[0])/1000000,float(p[1])/1000000)
#             i+=1
#             if(maxPoints >=512):
#                 print('Max points exceeded %d'%maxPoints)
#     partedPoints.append(pointUrl)
#     size = len(partedPoints)
#     print('Added %d points'%i)
#     print(size)
#     print(partedPoints[:5])
#     chunkNum = 11
#     chunkSize  = len(partedPoints)/chunkNum
#     print("Chunk Size %d"%chunkSize)
#     print("Chunk Num %d" %chunkNum)
#     partList = []
#      
#     for i in range(chunkNum):
#         with open('requestList%d'%i,'wb') as f:
#             print('chunk size ')
#             print(len(partedPoints[i*chunkSize:(i+1)*chunkSize+1]))
#             partList.append(partedPoints[i*chunkSize:(i+1)*chunkSize+1])
#             pickle.dump(partedPoints[i*chunkSize:(i+1)*chunkSize+1],f,2)
#             print("dumped %d"%i)  

# GOOGLE API
 
    http = urllib3.PoolManager()
    REQUESTNUMBER = 0
    with open('requestList%d'%REQUESTNUMBER,'rb') as f:
            tmp = pickle.load(f)
            print('LOADED SIZE %d'%len(tmp))
    size = len(tmp)
    count=0
    res = []
    for line in tmp:
        sleep(0.21)
        count+=1
        s = ELEVATION_BASE_URL + '?locations=' +  line[:-1] +"&key=" + KEY
        print(s)
           
        print ("REQUESTS : " + str(float(count)/size * 100))
        r = ''
        r = http.request_encode_url("GET", s)
        obj = simplejson.loads(r.data)
        with open('resultJson%d-%d.txt'%(REQUESTNUMBER,count),'a') as f:
            simplejson.dump(obj,f)
        if(obj['status'] == 'OK'):    
            print('OK')
            for resultSet in obj['results']:
                i = float(resultSet['location']['lat'])
                j = float(resultSet['location']['lng'])
                elev = float(resultSet['elevation'])
                with open('RESULTS%d.txt'%REQUESTNUMBER,'ab') as f:
                    f.write('%.7f,%.7f,%.7f\n'%(i,j,elev))
                res.append((i,j,elev))
        else:
            print("ERROR")
            print(obj['status'])
    with open('resultTestBckpTEST%d'%REQUESTNUMBER,'wb') as f:
        pickle.dump(res,f)
    print("DONE")

# LACZENIE WYNIKOW 
#     res = []
#     with open('FINALRESULT.txt','w') as result:
#         pass
#     with open('FINALRESULT.txt','a') as result:
#             
#         for i in range(8):
#             percent = -1.0
#             with open('RESULTS%d.txt'%i,'r') as f:
#                 lines = f.readlines()
#                 size = len(lines)
#                 for it in range(size):
#                     if(percent != round(float(it)/size *100)):
#                         percent = round(float(it)/size *100)
#                         print('%d : %d'%(i,percent) + os.linesep)
#                     result.write(lines[it])
