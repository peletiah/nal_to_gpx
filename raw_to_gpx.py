from lxml import etree
from xml.etree import ElementTree as ET
import codecs
import get_metadata
import os

def generate_metadata(root_element,gps_data):
    metadata_element = etree.Element("metadata")
    root_element.append(metadata_element)
    max_lat, min_lat, max_lon, min_lon = get_metadata.get_bounds(gps_data)
    bounds_element=etree.Element("bounds", maxlat = str(max_lat), maxlon = str(max_lon), minlat = str(min_lat), minlon = str(min_lon))
    metadata_element.append(bounds_element)

def generate_trk(root_element,gps_data):
    trk_element = etree.Element("trk")
    root_element.append(trk_element)
    trkpt_num = len(gps_data)
    distance = get_metadata.get_distance_vincenty(gps_data)
    duration = get_metadata.get_duration(gps_data)
    etree.SubElement(trk_element, "name").text = "Track 001"
    etree.SubElement(trk_element, "desc").text = "Total Track Points: {0}. Total time: {1}. Journey: {2:.3f}Km".format(trkpt_num, duration, distance)
    trkseg_element = etree.Element("trkseg")
    trk_element.append(trkseg_element)
    for trackpoint in gps_data: 
        generate_trkpt(trkseg_element, trackpoint)

def generate_timestamp(trkpt_element, trackpoint):
    timestamp = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z'.format(\
                 trackpoint['year'], \
                 trackpoint['month'], \
                 trackpoint['day'], \
                 trackpoint['hour'], \
                 trackpoint['minute'], \
                 trackpoint['second'])
    etree.SubElement(trkpt_element, "time").text = timestamp


def generate_trkpt_desc(trkpt_element, trackpoint):
    trkpt_desc = 'Lat.={0}, Long.={1}, Alt.={2}m., Speed={3}Km/h, Course={4}deg.'.format(\
                 trackpoint['latitude'], \
                 trackpoint['longitude'], \
                 trackpoint['height'], \
                 trackpoint['speed'], \
                 trackpoint['compass'])
    etree.SubElement(trkpt_element, "desc").text = trkpt_desc
    
    
def generate_extensions(trkpt_element, trackpoint):
    extensions_element = etree.Element("extensions")
    ns_gpx = "http://gps.wintec.tw/xsd/"
    nsmap = { 'gpxx':ns_gpx}
    NS = 'http://www.w3.org/2001/XMLSchema-instance'
    location_attribute = '{%s}schemaLocation' % NS
    location_value = "http://gps.wintec.tw/xsd http://gps.wintec.tw/xsd/TMX_GpxExt.xsd"
    trkpt_extension_element = etree.Element("{%s}TrackPointExtension" % ns_gpx,nsmap=nsmap, \
                                      attrib={location_attribute: location_value})
    etree.SubElement(trkpt_extension_element, "{%s}Temperature" % ns_gpx).text = str(trackpoint['temperature'])
    etree.SubElement(trkpt_extension_element, "{%s}Pressure" % ns_gpx).text = str(trackpoint['pressure'])
    extensions_element.append(trkpt_extension_element)
    trkpt_element.append(extensions_element)


def generate_trkpt(trkseg_element, trackpoint):
    trkpt_element = etree.Element("trkpt", lat = str(trackpoint['latitude']), lon = str(trackpoint['longitude']))
    etree.SubElement(trkpt_element, "ele").text = str(trackpoint['height'])
    generate_timestamp(trkpt_element, trackpoint)
    generate_trkpt_desc(trkpt_element, trackpoint)
    generate_extensions(trkpt_element, trackpoint)
    trkseg_element.append(trkpt_element)
    


def generate_xml(gps_data):
    NS = 'http://www.w3.org/2001/XMLSchema-instance'
    location_attribute = '{%s}schemaLocation' % NS
    location_value = "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_overlay/0/3 http://www.topografix.com/GPX/gpx_overlay/0/3/gpx_overlay.xsd http://www.topografix.com/GPX/gpx_modified/0/1 http://www.topografix.com/GPX/gpx_modified/0/1/gpx_modified.xsd"
    root_element = etree.Element("gpx", version="1.0", creator="nal_to_gpx.py - Christian Benke", attrib={location_attribute: location_value}, xmlns = "http://www.topografix.com/GPX/1/1")
    generate_metadata(root_element,gps_data)
    generate_trk(root_element,gps_data)
    return root_element

def write_gpx_file(xml_tree, nal_filename):
    gpx_filename = os.path.splitext(nal_filename)[0]+'.gpx'
    file = codecs.open(gpx_filename, "w", "utf-8")
    file.write(etree.tostring(xml_tree, xml_declaration=True, pretty_print=True, encoding='utf-8'))
    file.close()    
    

