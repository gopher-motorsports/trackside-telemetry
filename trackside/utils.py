'''
Utility functions for trackside-telemetry-software package
Gopher Motorsports 2021
'''
import yaml

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

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
        thousands of times a second. We will be timing this
        function and it must complete in less than 0.001 of a second.
    """

    #store bad data in array
    #timestamp influxDB

    startBit = bytes[0:2]

    if startBit == b'7E':
        name = bytes[2:6]
        time = bytes[6:14]
        value = bytes[14:]
        filepath = "can_tester.yaml"
        data = yaml_loader(filepath)
        dic = data['parameters']
        for info in dic.values():
            if info['id'] == int(name, 16):
                return {info['human_readable_name']: int(value, 16), "time": int(time, 16)}
    else:
        return {'Error bytes': bytes}