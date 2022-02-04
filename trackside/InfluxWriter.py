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