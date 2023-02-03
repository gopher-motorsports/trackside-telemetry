#!/usr/bin/env python3

from cmath import e
from influxdb import InfluxDBClient

class InfluxWriterTemp:

    '''
        Class InfluxWriter
        write points to influxDB database
            Parameters:
                    self (self): self
    '''
    def __init__(self):
        self.ifuser = "admin"
        self.ifpass = "trackside"
        self.ifdb = "telemetry"
        self.ifhost = "134.84.24.73"
        self.ifport = 8086

        self.ifclient = InfluxDBClient(self.ifhost,
                            self.ifport,
                            self.ifuser,
                            self.ifpass,
                            self.ifdb)

    '''
        Writes dictionary to database

            Parameters:
                    self (self): self
                    body (dictionary): A dictionary of sensor readings that includes name, value, and time stamp

            Returns:
                    void
    '''
    def write(self,body):
        try:
            print(body)
            print(self.ifport)
            self.ifclient.write_points(body)
        except Exception as e:
            print(e)
