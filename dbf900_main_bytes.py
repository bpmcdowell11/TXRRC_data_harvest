# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:41:40 2020

@author: MBelobraydic
"""

from dbf900_formats_bytes import pic_yyyymmdd, pic_yyyymm, pic_numeric, pic_any, pic_signed

##From https://github.com/skylerbast/TxRRC_data
##Generates the block of bytes from the file.
## Should be added to dbf900_main_bytes when it is working
def yield_blocks(file, n):
    block_bytes = file.read(n)
    while block_bytes:
        yield block_bytes
        block_bytes = file.read(n)


def parse_record(record, layout):
    values = dict()

    for name, start, size, convert in layout:
        
        ##check for additional data for pic_signed method
        if '_' in str(size): ##check if size also includes the number of decimals "Size_Decimal"
            size_split = size.split('_')
            size = int(size_split[0])
            decimal = int(size_split[1])
            
        if convert == 'pic_yyyymmdd':
            values[name] = pic_yyyymmdd(record[start:start+size])
        elif convert == 'pic_yyyymm':
            values[name] = pic_yyyymm(record[start:start+size])
        elif convert == 'pic_numeric':
            values[name] = pic_numeric(record[start:start+size])
        elif convert == 'pic_signed':
            values[name] = pic_signed(record[start:start+size],name, decimal)
        else:
            values[name] = pic_any(record[start:start+size])

    return values