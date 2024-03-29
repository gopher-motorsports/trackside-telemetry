#!/usr/bin/env python3

import yaml
import datetime
import os
import pathlib
import struct


here = str(pathlib.Path(__file__).absolute())
filepath = here[:-8] + os.path.join("data","sensors.yaml")
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.FullLoader)

'''
        Parses a single packet from the car (DLM) 
        and returns it as a python dictionary with
        the key as the sensor name, and the value
        as the sensors reading

            Parameters:
                    packet (bytes): A bytes object that represents the data from the car
                    data (dictionary): A dictionary of the sensors.yaml file

            Returns:
                    dictionary: dictionary with keys as name, data, and time
    '''
def parse_packet(packet, data):
    #packet = packet.rstrip(bytes.fromhex("7e"))
    packet = packet.hex()
    # if startBit == b'7e':
    #Account for escape bytes
    while '7d' in packet:
        index = packet.index('7d')
        if packet[index + 2:index + 4] != '':
            result = int(packet[index + 2:index + 4], 16) ^ int('0x20', 16)
            packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
        else:
            result = int('0', 10) ^ int('0x20', 16)
            packet = packet[0:index] + '{:x}'.format(result) + packet[index + 4:]
    
        
    if packet != b'' and len(packet) - 2 >= 14:
        time = int(packet[0:8], 16)
        name = int(packet[8:12], 16)
        dic = data['parameters']
        
        for info in dic.values():
            if info['id'] == name:
                try:
                    value_type = info['type']
                    nobytes = 0 
                    if(value_type == "UNSIGNED8"):
                        nobytes = 1
                        structFormat = '>B'
                    elif(value_type == "UNSIGNED16"):
                        nobytes = 2
                        structFormat = '>H'
                    elif(value_type == "UNSIGNED32"):
                        nobytes = 4
                        structFormat = '>I'
                    elif(value_type == "UNSIGNED64"):
                        nobytes = 8
                        structFormat = '>Q'
                    elif(value_type == "SIGNED8"):
                        nobytes = 1
                        structFormat = '>b'
                    elif(value_type == "SIGNED16"):
                        nobytes = 2
                        structFormat = '>h'
                    elif(value_type == "SIGNED32"):
                        nobytes = 4
                        structFormat = '>i'
                    elif(value_type == "SIGNED64"):
                        nobytes = 8
                        structFormat = '>q'     
                    elif(value_type == "FLOATING"):
                        nobytes = 4
                        structFormat = '>f'
                    end = 12 + nobytes * 2
                    value = packet[12:end]
                    value = struct.unpack(structFormat, bytes.fromhex(value))[0]
                    return {"name": info['motec_name'], "data": value, "time": time, "metadata_id": 0}
                   
                except ValueError as ve:
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":ve, "metadata_id": 0}
                except struct.error as error:
                    print(error)
                    return {"name": 'Error bytes', "data": packet, "time": time, "Message":error, "metadata_id": 0}
    else:
        return {"name": 'Error bytes', "data": packet, "time": datetime.datetime.utcnow(), "metadata_id": 0}
