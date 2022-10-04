#!/usr/bin/env python3

import yaml
import datetime
import os
import pathlib
import struct
import binascii


here = str(pathlib.Path(__file__).absolute())
filepath = here[:-8] + os.path.join("data","test.yaml")
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.FullLoader)

def parse_packet(packet, data):
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
    #packet = packet.rstrip(bytes.fromhex("7e"))
    packet = packet.hex()
    startBit = packet[0:2]
    # if startBit == b'7e':
    #Account for escape bytes
    while '7d' in packet:
        index = packet.index('7d')
        result = int(packet[index + 2:index + 4], 16) ^ int('0x20', 16)
        packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
        
    if packet != b'' and len(packet) - 2 >= 14:
        time = int(packet[0:8], 16)
        name = int(packet[8:12], 16)
        dic = data['parameters']
        
        for info in dic.values():
            if info['id'] == name:
            # if info['id'] == int.from_bytes(name, "big"):
                # end_bytes = 8 * info['bytes'] + 14
                
                #value = struct.unpack('!f', bytes.fromhex(value))[0]
                try:
                   
                   value = packet[12:28]
                   value = struct.unpack('>d', binascii.unhexlify(value))[0]
                   
                   return {"name": info['motec_name'], "data": value, "time": time}
                   
                except ValueError as ve:
                   return {"name": 'Error bytes', "data": packet, "time": time, "Message":ve}
                except struct.error as error:
                   return {"name": 'Error bytes', "data": packet, "time": time, "Message":error}
    else:
        return {"name": 'Error bytes', "data": packet, "time": datetime.datetime.utcnow()}
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