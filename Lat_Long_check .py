#made by -prakhar gupta
'''
This program checks for valid Latitude and Longitude entries
It also check for those latitude entries which lie outside of the boundary of San Jose

For San Jose
Lat - 37.004 to  37.5881
Long- -122.5154 to -121.1201
'''



import xml.etree.cElementTree as ET
import pprint


OSMFILE = "san-jose_california.osm"

def latandlong(filename):
    w_lat_long = {'lat':0,'long':0}
    for event, elems in ET.iterparse(filename):
        for elem in elems.iter(filename):
            if not(37.0047<=float(elem.attrib['lat']) <37.5881) : #Latitude limits taken from Openstreetmap
                w_lat_long['lat'] += 1
            elif not (-122.5154<=float(elem.attrib['lon'])<=-121.1201):#Longitude Limits taken from openstreetmap
                w_lat_long['long'] += 1
    return w_lat_long
    
print "No of Incorrect lat and long",latandlong(OSMFILE)






