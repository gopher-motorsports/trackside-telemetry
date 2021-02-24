import pandas as pd
import numpy as np
from influxdb import DataFrameClient
import time


class Streamer:

    def __init__(this,
                user = 'root',
                password = 'root',
                dbname = 'trackside',   #having trouble on windows/debian/mac, nobody likes localhost
                protocol = "line",
                host = 'localhost',
                port = '8086',
                ):
                this.user = user
                this.password = password
                this.dbname = dbname
                this.protocol = protocol
                this.host = host
                this.port = port


    def csv_stream(this,file="data.csv"):
        
        client = DataFrameClient(this.host,this.port,this.user,this.password,this.dbname)
        client.create_database(this.dbname)
        
        data = pd.read_csv(file)
        data_chunks = np.array_split(data,data.size/40) # influx likes chunks
        
        print("Writing chunks:\n")
        print("---------------------------------------------------------\n\n")

        for i,chunk in enumerate(data_chunks):
            print("Writing chunk %d\n",i)
            client.write_points(chunk,"CarData",protocol=protocol,numeric_precision="full")
            sleep(0.5)  # emulating 2hz resolution
        
        print("\n\nAll chunks written. Printing an example summary (time,rpm) \n")
        
        rs = client.query()
        times = list(rs.get_points(measurement="Time"))
        rpms = list(rs.get_points(measurement="Engine RPM"))

        for t in times:
            print(t)
            print("\n")

        for r in rpms:
            print(r)
            print("\n")

    if __name__ == 'main':
        print("Streamer object created.")
