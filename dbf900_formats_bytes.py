# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:03:51 2020

@author: MBelobraydic

formatting dates, strings, decimals, and numbers
"""
import codecs
from datetime import datetime
from datetime import date
from array import array

##From https://github.com/skylerbast/TxRRC_data
##converts bytes to string through codecs decoding
## Should be added to dbf900_main_bytes when it is working
def ebc_decode(data):
    ebcdic_decoder = codecs.getdecoder('cp1140')
    decoded = ebcdic_decoder(data)
    val = decoded[0]
    return val

def pic_yyyymmdd(date):
    date = ebc_decode(date)
    #Changes format YYYYMMDD from a series of numbers to datetime object
    try:
        val = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')
    except ValueError:
        val = None
    return val
    
def pic_yyyymm(yyyymm):
    yyyymm = ebc_decode(yyyymm)
    #Changes format YYYYMM from a series of numbers to datetime object
    #makes the date the first day of the month
    try:
        val = date(year=int(yyyymm[0:4]), month=int(yyyymm[4:]), day=1).strftime('%m/01/%Y')
    except ValueError:
        val = None

    return val

def pic_numeric(num):
    num = ebc_decode(num)
    try: ##using a try to ensure the values passed are actually 0-9 with no other characters
        val = int(num)
    except:
        val = None

    return val

def pic_any(string): #need to confirm the numberof characters
    string  = ebc_decode(string)
    STRIP_PIC_X = True # Set this to False if trimming PIC X causes problems.
    val = str(string)
    if STRIP_PIC_X == True:
        val = val.strip()

    return val

def pic_signed(signed,name,decimal=0): #replacement for pic_latlong and pic_coord
    # Converts an EBCDIC Signed number to Python float
    # 'signed' must be EBCDIC-encoded raw bytes -- this will not work
    # if the data has been converted to ASCII.
    ## info here http://www.3480-3590-data-conversion.com/article-signed-fields.html
    signed_raw = array('B', signed);
    val = float(0);
    
    # Bytes 1 to n-1 are stored as plain EBCDIC encoded digits
    for i in signed_raw:
        val = val * 10 + (i & 0x0F)
    
   
    # If the penultimate nibble == 0xD, then the number is negative. Otherwise,
    # it is either positive or unsigned.
    val = (val * (-1 if signed_raw[-1] >> 4 == 0xD else 1)) / 10**decimal
    
    ##TXRRC signs longitude as a positive value with 0xC and requires transformation to a negative number
    if 'LONGITUDE' in name and val > 0: ##This is only appropriate for western hemisphere
        val = -val
    
    return val