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
import struct

from bcolors import bcolors


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
import serial
import datetime


# Use python3 DLMSimulator.py to run the loop
def main():
    p = DLM()
    interval = 1000     # Time value between packets
    total_sensors = 189 
    time_bytes = 0      # To be added on to the packet
    data_start = 1800
    data_end = 2700
    data_bytes_length = 0
    data_type = p.sensors_dict[p.name_list[sensor_id-1]]["type"]
    # Set the number of data bytes according to the data type of the chosen sensor
    if(data_type == "UNSIGNED8"):
        data_bytes_length = 1
        structFormat = '>B'
    elif(data_type == "FLOATING"):
        data_bytes_length = 4
        structFormat = '>f'
    elif(data_type == "UNSIGNED32"):
        data_bytes_length = 4
        structFormat = '>I'
    elif(value_type == "UNSIGNED16"):
        data_bytes_length = 2
        structFormat = '>H'
    # Sensor id
    sensor_bytes = (sensor_id).to_bytes(2, 'big').hex().encode('ascii')   
    prnt = 0

    while True:
        sensor_id = random.randrange(1,total_sensors+1)        # Pick a random sensor id.
        sensor = p.sensors_dict[p.name_list[sensor_id-1]]
        # print(sensor)

        data_type = p.sensors_dict[p.name_list[sensor_id-1]]["type"]
        # Set the number of data bytes according to the data type of the chosen sensor
        if(data_type == "UNSIGNED8"):
            structFormat = '>B'
        elif(data_type == "FLOATING"):
            structFormat = '>f'
        elif(data_type == "UNSIGNED32"):
            structFormat = '>I'

        packet = struct.pack('>b', int('7e', 16)) #start packet with 7e (start bit)
        # packet += time_bytes.to_bytes(4, 'big').hex().encode('ascii')
        packet += struct.pack('>I', time_bytes)
        packet += struct.pack('>H', sensor_id)

        if(data_type == "UNSIGNED8"):
            dat = random.randrange(0,256)
            # packet += dat.to_bytes(data_bytes_length, 'big').hex().encode('ascii')
            # packet += (struct.pack(structFormat, dat)).hex().encode('ascii')
            packet += struct.pack(structFormat, dat)
        elif(data_type == "FLOATING"):
            dat = random.uniform(data_start,data_end)
            # packet += (struct.pack(structFormat, dat)).hex().encode('ascii')
            packet += struct.pack(structFormat, dat)
        elif(data_type == "UNSIGNED32"):
            dat = random.randrange(data_start,data_end)
            packet += (bytearray(struct.pack(structFormat, dat))).hex().encode('ascii')
        elif(data_type == "UNSIGNED16"):
            dat = random.randrange(data_start,data_end)
            packet += (bytearray(struct.pack(structFormat, dat))).hex().encode('ascii')
        print(packet)
        port = '/dev/ttyUSB0'
        speed = 9600
        ser = serial.Serial(port,speed)
        try:
            ser.write(packet)
            if prnt == 6:
                prnt = 0
                print( (bcolors.HEADER + "Logged point at: " + bcolors.ENDC) + bcolors.BOLD + (datetime.datetime.now().strftime("%H:%M:%S") + bcolors.ENDC))
                print(bcolors.OKGREEN + str(packet) + bcolors.ENDC + "\n")

            else:
                prnt += 1
        except KeyboardInterrupt:
            break
        time_bytes += interval
        time.sleep(0.5)

if __name__ == '__main__':
    main()