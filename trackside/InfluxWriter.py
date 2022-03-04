#!/usr/bin/env python3

from influxdb import InfluxDBClient

class InfluxWriter:
    """
    Class InfluxWriter
    Params: 
    self
    Purpose: 
    to easily write points to influxDB database
    """
    def __init__(self):
        self.ifuser = "trackside"
        self.ifpass = "trackside"
        self.ifdb = "trackside"
        self.ifhost = "172.17.0.1"
        self.ifport = 8086
        measurement_name = "system"

        self.ifclient = InfluxDBClient(self.ifhost,
                            self.ifport,
                            self.ifuser,
                            self.ifpass,
                            self.ifdb)

    def write(self,body):
        self.ifclient.write_points(body)
        
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
