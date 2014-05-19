from decimal import Decimal
from haversine_calculation import haversine

def get_bounds(gps_data):
    num_trkpts = len(gps_data)
    max_lat = Decimal(90)
    min_lat = Decimal(-90)
    max_lon = Decimal(180)
    min_lon = Decimal(-180)
 
    max_lat_tmp = min_lat
    min_lat_tmp = max_lat
    max_lon_tmp = min_lon
    min_lon_tmp = max_lon
    
    for trkpt in gps_data:
        if trkpt['latitude'] >= max_lat_tmp:
            max_lat_tmp = trkpt['latitude']
   
        if trkpt['latitude'] <= min_lat_tmp:
            min_lat_tmp = trkpt['latitude']
        
        if trkpt['longitude'] >= max_lon_tmp:
            max_lon_tmp = trkpt['longitude']

        if trkpt['longitude'] <= min_lon_tmp:
            min_lon_tmp = trkpt['longitude']
        
    max_lat = max_lat_tmp
    min_lat = min_lat_tmp
    max_lon = max_lon_tmp
    min_lon = min_lon_tmp
    return max_lat, min_lat, max_lon, min_lon

def get_distance(gps_data):
    distance = 0
    last_trkpt = gps_data[0]
    n = 0
    for trkpt in gps_data:
        n = n+1
        #if last_trkpt['timestamp'] != trkpt['timestamp']:
        distance = distance + haversine(last_trkpt['latitude'],last_trkpt['longitude'],trkpt['latitude'],trkpt['longitude'])
        print '#',n,distance
        last_trkpt=trkpt
    return distance
         
    
