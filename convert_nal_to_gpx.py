#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decode_nal
import raw_to_gpx
import sys

def main():
    #nal_file = open('20131203_05_42_31.NAL')

    for arg in sys.argv[1:]:
        print 'Opening ' + arg
        nal_file = open(arg)
        nal_bin_data=nal_file.read()
        
        block_number = decode_nal.num_blocks(nal_bin_data)
        print "Number of blocks:", block_number
        
        nal_decoded_data=list()

        for block_index in range( decode_nal.num_blocks(nal_bin_data) ):
            offset = decode_nal.get_offset(block_index)
            nal_decoded = decode_nal.decode(nal_bin_data,offset)
            nal_decoded_data.append(nal_decoded)
        print nal_decoded_data[0]['latitude']
        gpx_tree = raw_to_gpx.generate_xml(nal_decoded_data)
        raw_to_gpx.write_gpx_file(gpx_tree, arg)
        

if __name__=='__main__':
    main()
