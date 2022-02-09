'''
DLM Simulator for off-season development
Gopher Motorsports 2021
'''

import binascii
import random
import configparser
import yaml
import datetime

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
    def random_bytes(self, sensor_name, sensors_dict):
        packet = random.randrange(0,100).to_bytes(sensors_dict[sensor_name]['bytes'],'big')

        return binascii.hexlify(packet)
    
    def __init__(self,speed=1000,seed=69,errors=0.01):

        ## Hz of output, eg 1000 packets per second
        self.speed = speed 

        ## Random seed: Seed to supply to random for repeatable results
        random.seed(a=seed)

        ## Percentage of corrupted packets: 0.01 = 1% of packets corrupted
        self.errors = errors

        ## Current packet: contains current packet to be sent. updated speed times a second
        self.packet = None

        #Read sensors from trackside.ini
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('../trackside.ini')
        sensor_list_tuple = list(config.items('sensors'))
        sensor_list = []

        for i in sensor_list_tuple:
            sensor_list.append(int(i[0]))

        #Parse Sensor Yaml

        filepath = "./data/go4-22c.yaml"
        #global variable
        file_descriptor = open(filepath, "r")  
        data = yaml.load(file_descriptor, yaml.FullLoader)
        
        params = data['parameters']
        sensors_dict = {}
        for sensor_id in sensor_list:
            for id in params.values():
                if(id['id'] == sensor_id):
                    sensors_dict[id['name']] = id
        print(DLM.random_bytes(self, 'ambient_air_temperature', sensors_dict))
        

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
        '''
        Main runtime.
        '''

        self.packet = self.rpm_idle()

    def __repr__(self):
        ## String representation of class
        return "Current packet: {packet}".format(packet = self.packet)


    @property
    def data(self):
        ## Allows someone to call "DLM.data" and get
        ## the current packet
        return self.packet
