'''
Utility functions for trackside-telemetry-software package
Gopher Motorsports 2021
'''
import yaml
import datetime

filepath = "./can_tester.yaml"
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.Loader)


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

    ## FIX: Time variable is a <class 'datetime.datetime'> object, this is incorrect
    time = datetime.datetime.utcnow()
    #print(type(time))

    if startBit == b'7E':
        name = bytes[2:6]
        value = bytes[14:]
        filepath = "can_tester.yaml"
        dic = data['parameters']
        for info in dic.values():
            if info['id'] == int(name, 16):
                return {info['human_readable_name']: int(value, 16), "time": time}
    else:
        return {'Error bytes': bytes, "time": time}