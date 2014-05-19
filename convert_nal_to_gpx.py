#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decode_nal

def main():
    nal_file = open('../20131203_05_42_31.NAL')
    nal_bin_data=nal_file.read()
    
    block_number = decode_nal.num_blocks(nal_bin_data)
    print "Number of blocks:", block_number
    
    nal_decoded_data=list()

    for block_index in range( decode_nal.num_blocks(nal_bin_data) ):
        offset = decode_nal.get_offset(block_index)
        nal_decoded = decode_nal.decode(nal_bin_data,offset)
        nal_decoded_data.append(nal_decoded)
    return nal_decoded_data

if __name__=='__main__':
    main()
