from influxdb import InfluxDBClient

class InfluxWriter:
    def __init__(self):
        self.ifuser = "trackside"
        self.ifpass = "trackside"
        self.ifdb = "trackside"
        self.ifhost = "172.17.0.1"
        self.ifport = 8086
        measurement_name = "system"

    def write(self,body):
        
        ifclient = InfluxDBClient(self.ifhost,
                                  self.ifport,
                                  self.ifuser,
                                  self.ifpass,
                                  self.ifdb)
        ifclient.write_points(body)