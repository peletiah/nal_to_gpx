from lxml import etree
from xml.etree import ElementTree as ET
import codecs
import get_metadata
import os
from datetime import timedelta, datetime


field_names= ('type','padding1','timestamp','second','minute','hour','day','month','year','latitude','longitude','height','temperature','pressure','cadence','pulse','slope','compass','roll','yaw','speed','bike','padding2','padding3')


def main():
    gpxfile = '/home/benke/wsg2000_conversion/env/nal_to_gpx/gilgit.gpx'
    file = open(gpxfile,'r')

    trkpt_list=list()
    start_time = datetime.strptime('2013-11-05 09:19:03', "%Y-%m-%d %H:%M:%S")
    curr_time = start_time
    delta = timedelta(seconds=10)
    
    gpx_ns = "http://www.topografix.com/GPX/1/0"
    root = etree.parse(file).getroot()
    trackSegments = root.getiterator("{%s}trkseg"%gpx_ns)
    for trackSegment in trackSegments:
        for trackPoint in trackSegment:
            curr_time = curr_time + delta
            lat=trackPoint.attrib['lat']
            lon=trackPoint.attrib['lon']
            trkpt_list.append({ \
                    'type': 0, \
                    'padding' : 0, \
                    'timestamp' : 0, \
                    'second' : int(curr_time.strftime('%S')), \
                    'minute' : int(curr_time.strftime('%M')), \
                    'hour' : int(curr_time.strftime('%H')), \
                    'day' : int(curr_time.strftime('%d')), \
                    'month' : int(curr_time.strftime('%m')), \
                    'year' : int(curr_time.strftime('%Y')), \
                    'latitude' : lat, \
                    'longitude' : lon, \
                    'height' : 1788, \
                    'temperature' : 22, \
                    'pressure' : 832, \
                    'cadence' : 0, \
                    'pulse' : 0, \
                    'slope' : 0, \
                    'compass' : 0, \
                    'roll' : 0, \
                    'yaw' : 0, \
                    'speed' : 15, \
                    'bike' : 0, \
                    'padding2' : 0, \
                    'padding3' : 0 \
                    })
        return trkpt_list    
            


if __name__=='__main__':
    main()
