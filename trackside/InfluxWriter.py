#!/usr/bin/env python3

from cmath import e
from influxdb import InfluxDBClient

class InfluxWriter:

    '''
        Class InfluxWriter
        write points to influxDB database
            Parameters:
                    self (self): self
    '''
    def __init__(self):
        self.ifuser = "root"
        self.ifpass = "trackside"
        self.ifdb = "trackside"
        self.ifhost = "influxdb"
        self.ifport = 8086
        measurement_name = "system"

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
            self.ifclient.write_points(body)
        except Exception as e:
            print(e)
        
    '''write from csv, still under development'''
    def write_csv(self,fname):
        import datetime
        import os

        fp = open(os.path.join(os.getcwd(),fname),"r")
        fieldlist = fp.readline().split(',')
        fields = {}
        
        for line in fp.readlines()[1:]:
            datas = line.split(',')
            for i,field in enumerate(fieldlist):
                fields[field] = float(datas[i])
            
            time = datetime.datetime.utcnow()
            body = [
                    {
                        "measurement": "system",
                        "time": time,
                        "fields": fields
                    }
                ]
        
            self.write(body)
            fields = {}
