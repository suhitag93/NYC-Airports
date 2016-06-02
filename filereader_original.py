import spatial
import time
from rtree import index

a = 'taxigreen(06-15)_table.csv'
b = 'sample-taxi-data.csv'
c = 'neighborhoods.txt'

start_time = time.time()
def Read_Airport():
    JFK=[]
    LGA=[]
    #Fill JFK:
    with open(c) as file:
        stop = int(file.readlines()[1])+2
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

jfk, lga =Read_Airport()


jfk_count =0

lga_count =0

with open(a) as f:
    for line in f.readlines()[2:]:
        line = line.strip()
        plat, plon, dlat, dlon, d_pickup, d_dropoff, distance = line.split(',')
        drop = spatial.Point(float(dlat),float(dlon)) #drop off location in Poin object
        if jfk.contains(drop):
            jfk_count+=1
        elif lga.contains(drop):
            lga_count+=1
            # print('trip is dropping off at JFK')

print("JFK: ",str(jfk_count))
print("LGA: ",str(lga_count))
print("--- %s seconds ---" % (time.time() - start_time))

jfk_bounds = jfk.bounds()
lga_bounds = lga.bounds()

#RTREE:
def RTree():
    #result=[]
    with open(a) as f:
        idx =index.Index()
        i=0
        for line in f.readlines()[2:]:
            i+=1
            line = line.strip()
            plat, plon, dlat, dlon, d_pickup, d_dropoff, distance = line.split(',')
            dlat=float(dlat)
            dlon=float(dlon)
            idx.insert(i,(dlat,dlon))
        jfk_result= list(idx.intersection(jfk_bounds))
        lga_result = list(idx.intersection(lga_bounds))
        #print result
        print 'JFK: '
        print len(jfk_result)
        print 'LGA: '
        print len(lga_result)

RTree()