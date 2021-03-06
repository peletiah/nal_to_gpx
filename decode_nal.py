#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
from itertools import starmap
from functools import partial
from decimal import Decimal


"""

NAL format definition via http://www.mikrocontroller.net/topic/260568


typedef struct nal_data32 {
  unsigned char point_type; /* 0 - normal, 1 - start, 2 - marked */

  unsigned char padding_1;

  unsigned int second: 6, minute: 6, hour: 5;
  unsigned int day: 5, month: 4, year: 6; /* add 2000 to year */

  signed int latitude;    /* divide by 1E7 for degrees */
  signed int longitude;   /* divide by 1E7 for degrees */

  unsigned short height;    /* meters */

  signed char temperature;  /* °C */

  unsigned short pressure;  /* mbar */

  unsigned char cadence;    /* RPM */
  unsigned char pulse;    /* BPM */

  signed char slope;    /* degrees */

  signed short compass;   /* °Z axis */
  signed short roll;    /* °X axis */
  signed short yaw;   /* °Y axis */

  unsigned char speed;    /* km/h */

  unsigned char bike;   /* ID# 0-3 */

  unsigned char padding_2;
  unsigned char padding_3;
}

"""

#TODO speed has a value of 0 if no bike-sensor is present (GPS-mode only)

#Fixed blocksize of 32 Byte
blocksize = 32

#Format declaration in short form
format = '<BBIiihbHBBbhhhBBBB' 

#Offset-declaration for the 32bit time-field
width_offsets = [(6,0),(6,6),(5,12),(5,17),(4,22),(6,26)] 

field_names= ('type','padding1','timestamp','latitude','longitude','height','temperature','pressure','cadence','pulse','slope','compass','roll','yaw','speed','bike','padding2','padding3')

time_names = ('second','minute','hour','day','month','year')

def unmask(num, width, offset):
     return (num & (2**width - 1) << offset) >> offset

def num_blocks(data):
    # How many packets are in data
    # Make sure we have an even number of datagrams
    assert (len(data) % blocksize == 0)
    return len(data) / blocksize


def get_offset(block_number):
    # Calculate the starting offset of a block
    return block_number * blocksize

def decode(data, offset=0):
    data_values = struct.unpack(format,data[offset : offset + 32])
    nal_dict = dict(zip (field_names, data_values))
   
    # decode the timestamp-bitfield with unmask()
    # http://stackoverflow.com/questions/23723151/converting-binary-timestamp-to-string
    time_values = list(starmap(partial(unmask,nal_dict['timestamp']), width_offsets))
    time_dict = dict(zip (time_names, time_values))
    time_dict['year']=time_dict['year']+2000

    nal_dict = dict(nal_dict.items() + time_dict.items())

    # latitude/longitude have to be divided by 10000000 for decimal-format
    nal_dict['longitude'] = Decimal(nal_dict['longitude']) / 10000000
    nal_dict['latitude'] = Decimal(nal_dict['latitude']) / 10000000

    return nal_dict


