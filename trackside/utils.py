'''
Utility functions for trackside-telemetry-software package
Gopher Motorsports 2021
'''
import yaml
import datetime

filepath = "./data/go4-22c.yaml"
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
    Reqs: 
        Minimal overhead, this function will run
        many of times a second. We will be timing this
        function and it must complete in less than 0.01 of a second.
    """


    startBit = bytes[0:2]

    time = datetime.datetime.utcnow()
    
    if startBit == b'7e':
        time = bytes[2:10]
        name = bytes[10:14]

        dic = data['parameters']

        for info in dic.values():
            if info['id'] == int(name, 16):
                #end_bytes = 8 * info['bytes'] + 14
                value = bytes[14:22]
                try:
                    return {info['human_readable_name']: int(value, 16), "time": time}
                except ValueError as ve:
                    return {'Error bytes': bytes, "time": time, "Message":ve}

    else:
        return {'Error bytes': bytes, "time": time}