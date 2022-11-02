#!/usr/bin/env python3
'''
DLM Simulator for off-season development
Gopher Motorsports 2021
'''


import binascii
import random
import configparser
import yaml
import pathlib
import os


class DLM:
    """
    Class:
        DLM
    Params: 
        self
        speed
        seed
    Purpose: 
        to simulate the DLM (car) during driving, to
        allow off-season development of the trackside 
        telemetry package. 
    Reqs:
        Must produce randomly chosen packets in the exact format
        as will be sent from the DLM over the XBEEs to the 
        rpi. A percentage of these packets should be corrupted 
        to test reliability of the system. 
    """
    
    def __init__(self,speed=1000,seed=69,errors=0.01):

        ## Hz of output, eg 1000 packets per second
        self.speed = speed 

        ## Random seed: Seed to supply to random for repeatable results
        # random.seed(a=seed)

        ## Percentage of corrupted packets: 0.01 = 1% of packets corrupted
        self.errors = errors

        ## Current packet: contains current packet to be sent. updated speed times a second
        self.packet = None

        self.sensors_dict = {}

        #Parse Sensor Yaml
        # here = str(pathlib.Path(__file__).absolute())
        # filepath = here[:-15] + os.path.join("data","go4-22c.yaml")
        filepath = "data/sensors.yaml"
        #global variable
        file_descriptor = open(filepath, "r")  
        data = yaml.load(file_descriptor, yaml.FullLoader)
        params = data['parameters']
        for id in params.values():
            self.sensors_dict[id['name']] = id
        self.name_list = list(self.sensors_dict.keys())

    def random_bytes(self, sensor_name):
        packet = bytes.fromhex('7E')
        packet += bytes.fromhex('00000000')
        
        id = self.sensors_dict[sensor_name]['id']
        packet += id.to_bytes(2, 'big')
        val = random.randrange(0,100)
        packet += val.to_bytes(4, 'big')

        return packet.hex().encode('ascii')

    def rpm_idle(self):
        packet = None
        if(random.random() <= self.errors):
            packet = random.randrange(0,200000000).to_bytes(11,'big')
        else:
            packet = b'7E'
        packet += b'000100000000'

        rpm = random.randrange(1800,2700)
        packet += hex(rpm)[2:].encode('ascii')
        
        return packet
    
    def run(self):
        self.packet = self.random_bytes(random.choice(self.name_list))

    def __repr__(self):
        ## String representation of class
        return "Current packet: {packet}".format(packet = self.packet)

    @property
    def data(self):
        ## Allows someone to call "DLM.data" and get
        ## the current packet
        return self.packet

import time


# Use python3 DLMSimulator.py to run the loop
def main():
    p = DLM()
    interval = 1000     # Time value between packets
    total_sensors = 189 
    time_bytes = 0      # To be added on to the packet

    sensor = random.randrange(1,total_sensors+1)        # Pick a random sensor id.
    # sensor = 1
    print(p.sensors_dict[p.name_list[sensor-1]])
    # Sensor data interval to randomly choose bytes from.
    data_start = 1800
    data_end = 2700
    data_bytes_length = 4
    # Sensor id
    sensor_bytes = (sensor).to_bytes(2, 'big').hex().encode('ascii')   
    while True:
        packet = b'7e'
        packet += time_bytes.to_bytes(4, 'big').hex().encode('ascii')
        packet += sensor_bytes

        dat = random.randrange(data_start,data_end)
        packet += dat.to_bytes(data_bytes_length, 'big').hex().encode('ascii')
        print(packet)
        time_bytes += interval
        time.sleep(1)

if __name__ == '__main__':
    main()