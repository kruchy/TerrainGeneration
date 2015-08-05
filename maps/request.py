import urllib3
import simplejson
from time import sleep
import pickle
ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
class Request(object):

    poolmanager = None
    
    def __init__(self):
        self.poolmanager = urllib3.PoolManager()
        
        
    def requestFromList(self,points,key):
        pointUrl = '' 
        partedPoints = []
        urlList = []
        baseUrl =ELEVATION_BASE_URL + '?locations=' +"&key=" + key 
        maxPoints = 0
        i = 0
        for p in points:
            maxPoints += 0
            if(len(pointUrl + '%.7f,%.7f|'%(float(p[0])/1000000,float(p[1])/1000000)) + len(baseUrl)< 2000):
                pointUrl += '%.7f,%.7f|'%(float(p[0]),float(p[1]))
                maxPoints +=1
                i+=1
                if(maxPoints >=512):
                    print('Max points exceeded %d'%maxPoints)
            else:
                partedPoints.append(pointUrl)
                pointUrl = ''
                maxPoints = 1
                pointUrl += '%.7f,%.7f|'%(float(p[0])/1000000,float(p[1])/1000000)
                i+=1
                if(maxPoints >=512):
                    print('Max points exceeded %d'%maxPoints)
        partedPoints.append(pointUrl)
        size = len(partedPoints)
        return partedPoints
        
    def elevationRequest(self,list,key):
        size = len(list)
        count=0
        res = []
        for line in list:
            sleep(0.21)
            count+=1
            s = ELEVATION_BASE_URL + '?locations=' +  line[:-1] +"&key=" + key
            print(s)
               
            print ("REQUESTS : " + str(float(count)/size * 100))
            r = ''
            r = self.poolmanager.request_encode_url("GET", s)
            obj = simplejson.loads(r.data)
            with open('resultJson-%d.txt'%count,'a') as f:
                simplejson.dump(obj,f)
            if(obj['status'] == 'OK'):    
                print('OK')
                for resultSet in obj['results']:
                    i = float(resultSet['location']['lat'])
                    j = float(resultSet['location']['lng'])
                    elev = float(resultSet['elevation'])
                    with open('RESULTS.txt','ab') as f:
                        f.write('%.7f,%.7f,%.7f\n'%(i,j,elev))
                    res.append((i,j,elev))
            else:
                print("ERROR")
                print(obj['status'])
        with open('resultBckp','wb') as f:
            pickle.dump(res,f)
        print("DONE")