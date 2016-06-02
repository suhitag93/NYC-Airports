import spatial
import time
from rtree import index

main_file = 'taxigreen(06-15)_table.csv'
sample = 'sample-taxi-data.csv'
locations = 'neighborhoods.txt'


def Read_Airport(start):
    L = []  # empty list to store location values
    with open(locations) as file:
        stop = int(file.readlines()[start-1])
        #print stop
        with open(locations) as f:
            for line in f.readlines()[start:start+stop]:
                line = line.strip();
                # print line
                lon, lat = line.split(',')
                lon = float(lon)
                lat = float(lat)
                L.append(spatial.Point(lat, lon))  # append lat-long coordinates in spatial form
    poly = spatial.Polygon(L)  # create polygon
    return poly

def Maplocations(poly):
    start_time = time.time()
    poly_list = []
    with open(main_file) as f:
        for line in f.readlines()[2:]:
            line = line.strip()
            plat, plon, dlat, dlon, d_pickup, d_dropoff, distance = line.split(',')
            drop = spatial.Point(float(dlat), float(dlon))  # convert drop off location in Point object
            if poly.contains(drop):
                poly_list.append(drop)
    print " Number of drop locations %s" %(len(poly_list))
    end_time = time.time() - start_time
    return poly_list,end_time


def create_RTree():
    idx = index.Index()
    i = 0
    L = []
    f=open(main_file)
    for line in f.readlines()[2:]:
            line = line.strip()
            plat, plon, dlat, dlon, d_pickup, d_dropoff, distance = line.split(',')
            dlat = float(dlat)
            dlon = float(dlon)

            L.append(spatial.Point(dlat,dlon)   ) #keep track of drop off points
            idx.insert(i, (dlat, dlon))
            i += 1
    return idx, L

# RTREE:
def RTree(poly,idx, L):

    output = []
    start_time = time.time()
    result = list(idx.intersection(poly.bounds()))
    print " RTree:"
    print " # Within bounds: " + str(len(result))
    for j in result:
        if poly.contains(L[j]):
            output.append(L[j])
    print " # Filtered locations:" + str(len(output))
    end_time = time.time()-start_time
    return output,end_time

def main():
    print "----JFK----"
    drop_Index,drop_List = create_RTree()

    # JFK spatial polygon
    jfk = Read_Airport(2)
    print "Part 2:"
    Loc_jfk, jfk_map_end = Maplocations(jfk)
    print " %s seconds to complete" %(jfk_map_end)
    print "Part 5. a) JFK"
    jfk_tree, jfk_tree_end=RTree(jfk,drop_Index,drop_List)
    print " RTree run: %s seconds" % (jfk_tree_end)
    # LGA spatial polygon
    print"\n\n"
    print "----LGA-----"
    # LGA spatial polygon

    lga = Read_Airport(30)
    print "Part 3:"
    Loc_jfk, lga_map_end = Maplocations(lga)
    print " %s seconds to complete" %(lga_map_end)
    print "Part 5: b) LGA"
    lga_tree, lga_tree_end=RTree(lga,drop_Index,drop_List)
    print " RTree run: %s seconds" % (lga_tree_end)

if __name__ == "__main__":
    main()