import spatial
import time
from rtree import index


a = 'taxigreen(06-15)_table.csv'
b = 'sample-taxi-data.csv'
c = 'neighborhoods.txt'

def Read_Airport():

    JFK=[]
    LGA=[]
    #Fill JFK:

    with open(c) as file:
        stop = int(file.readlines()[1]) +2
        #print stop
        with open(c) as f:
            for line in f.readlines()[2:stop]:
                line = line.strip();
                #print line
                lon, lat = line.split(',')
                lon = float(lon)
                lat = float(lat)
                JFK.append(spatial.Point(lat,lon))
        #LGA

        start = stop+3
        with open(c) as f:
            #print f.readlines()[start]
            for line in f.readlines()[start:]:
                line = line.strip()
                lon, lat = line.split(',')
                lon = float(lon)
                lat = float(lat)
                #print line
                LGA.append(spatial.Point(lat,lon))
        jfk_poly = spatial.Polygon(JFK)
        lga_poly = spatial.Polygon(LGA)
    return jfk_poly,lga_poly



def RTree():
    jfk , lga = Read_Airport()
    with open(b) as f:
        idx =index.Index()
        i=0
        jfk_out = []
        lga_out = []
        L = []
        for line in f.readlines()[2:]:

            line = line.strip()
            plat, plon, dlat, dlon, d_pickup, d_dropoff, distance = line.split(',')
            dlat=float(dlat)
            dlon=float(dlon)
            idx.insert(i,(dlat,dlon))
            L.append(spatial.Point(dlat, dlon))
            i+=1
            lga_result = list(idx.intersection(lga.bounds()))
            jfk_result = list(idx.intersection(jfk.bounds()))
        print "Within JFK bounds: "+str(len(jfk_result))
        for j in jfk_result:
            if jfk.contains(L[j]):
                jfk_out.append(L[j])
        print "JFK Filtered locations:"+str(len(jfk_out))
        print "Within LGA bounds: "+str
        for j in lga_result:
            if lga.contains(L[j]):
                lga_out.append(L[j])
        print len(lga_out)
        #print len(lga_result)


def main():
    jfk_start = time.time()
    jfk, lga = Read_Airport()       #get location polygons


RTree()