#!/usr/bin/env python3

import yaml
import datetime
import os
import pathlib


here = str(pathlib.Path(__file__).absolute())
filepath = here[:-8] + os.path.join("data","go4-22c.yaml")
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
    if startBit == b'7e':
        time = bytes[2:10]
        name = bytes[10:14]
        dic = data['parameters']

        for info in dic.values():
            if info['id'] == int(name, 16):
                #end_bytes = 8 * info['bytes'] + 14
                value = bytes[14:22]
                try:
                    return {"name": info['human_readable_name'], "data": int(value, 16), "time": time}
                except ValueError as ve:
                    return {'Error bytes': bytes, "time": time, "Message":ve}
    else:
        return {'Error bytes': bytes, "time": time}
