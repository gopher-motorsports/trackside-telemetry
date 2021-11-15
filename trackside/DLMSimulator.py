'''
DLM Simulator for off-season development
Gopher Motorsports 2021
'''

import random

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
        random.seed(a=seed)

        ## Percentage of corrupted packets: 0.01 = 1% of packets corrupted
        self.errors = errors

        ## Current packet: contains current packet to be sent. updated speed times a second
        self.packet = None


    def rpm_idle(self):
        packet = None
        if(random.random() <= self.errors):
            packet = random.randrange(0,200000000).to_bytes(11,'big')
        else:
            packet = b'7E'
        packet += b'000100000000'

        rpm = random.randrange(1500,3000)
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
