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
        self.seed = seed

        ## Percentage of corrupted packets: 0.01 = 1% of packets corrupted
        self.errors = errors

        ## Current packet: contains current packet to be sent. updated speed times a second
        self.packet = None

    
    def run(self):
        '''
        Main runtime.
        '''
        # TODO
        print("hello world")



    def __repr__(self):
        ## String representation of class
        return f"Current packet: {self.packet}"


    @property
    def data(self):
        ## Allows someone to call "DLM.data" and get
        ## the current packet
        return self.packet


    def __main__(self):
        self.run()
