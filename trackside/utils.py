#!/usr/bin/env python3

import yaml
import datetime
import os
import pathlib


here = str(pathlib.Path(__file__).absolute())
filepath = here[:-8] + os.path.join("data","can_tester.yaml")
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.FullLoader)

def parse_packet(bytes):
    """
    Function: 
        parse_packet
    Params:
        bytes - bytes object to be parsed (one sensors data for a frame)
    Purpose: 
        To parse a single packet from the car (DLM) 
        and return it as a python dictionary with
        the key as the sensor name, and the value
        as the sensors reading
    """
    time = datetime.datetime.utcnow()
    startBit = bytes[0:2]
    #if startBit == b'7e':
    if True:
        time = bytes[2:10]
        name = bytes[10:14]
        dic = data['parameters']

        for info in dic.values():
           if info['id'] == int(name, 16):
                end_bytes = 8 * info['bytes'] + 14
                value = bytes[14:22]
                try:
                   return {"name": info['human_readable_name'], "data": float(value), "time": time}
                except ValueError as ve:
                   return {"name": 'Error bytes', "data": bytes, "time": time, "Message":ve}
    else:
        return {"name": 'Error bytes', "data": bytes, "time": time}
#    # remove start delimiter from byte string
#     byteStr = packet.rstrip(bytes.fromhex("7e"))
#     pkt = []
#     # escape & append bytes
#     escNext = False
#     for byte in byteStr:
#         if escNext:
#             pkt.append(byte ^ 0x20)
#             escNext = False
#         elif (byte == int("7d", base=16)):
#             escNext = True
#         else:
#             pkt.append(byte)
#             escNext = False
#     # convert to hex strings
#     return [hex(byte) for byte in pkt]