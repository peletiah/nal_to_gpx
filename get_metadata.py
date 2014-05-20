from decimal import Decimal
from datetime import timedelta, datetime
from geopy.distance import VincentyDistance, GreatCircleDistance


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


# Most accurate geodesic distance calculation
# using the Thaddeus Vincenty formula
def get_distance_vincenty(gps_data):
    distance = 0
    last_trkpt = [gps_data[0]['latitude'],gps_data[0]['longitude']]
    for trkpt in gps_data:
        curr_trkpt = [trkpt['latitude'],trkpt['longitude']]
        dist = VincentyDistance()
        distance = distance + dist.measure(last_trkpt,curr_trkpt)
        last_trkpt = curr_trkpt
    return distance
       
# Less accurate geodesic distance calculation 
# via Earth radius (Sphere)
def get_distance_great_circle(gps_data):
    distance = 0
    last_trkpt = [gps_data[0]['latitude'], gps_data[0]['longitude']]
    for trkpt in gps_data:
        curr_trkpt = [trkpt['latitude'], trkpt['longitude']]
        dist = GreatCircleDistance()
        distance = distance + dist.measure(last_trkpt,curr_trkpt)
        last_trkpt = curr_trkpt
    return distance
 
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

 
def get_duration(gps_data):
    first_timestamp='{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(\
                    gps_data[0]['year'], \
                    gps_data[0]['month'], \
                    gps_data[0]['day'], \
                    gps_data[0]['hour'], \
                    gps_data[0]['minute'], \
                    gps_data[0]['second'])
    last_timestamp='{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(\
                    gps_data[-1]['year'], \
                    gps_data[-1]['month'], \
                    gps_data[-1]['day'], \
                    gps_data[-1]['hour'], \
                    gps_data[-1]['minute'], \
                    gps_data[-1]['second'])
    time_first=datetime.strptime(first_timestamp, "%Y-%m-%d %H:%M:%S")
    time_last=datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
    duration = time_last - time_first
    return strfdelta(duration, "{hours}h{minutes}m{seconds}s")
