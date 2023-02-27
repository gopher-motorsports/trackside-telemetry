from utils import *
import time
import InfluxWriterTemp as iw

here = str(pathlib.Path(__file__).absolute())
filepath = here[:-10] + os.path.join("\\data","sensors.yaml")
#global variable
file_descriptor = open(filepath, "r")  
variable = yaml.load(file_descriptor, yaml.FullLoader)

# f = open("dlm_data_20210413_004735.gdat", "rb")
with open("dlm_data_20210413_004735.gdat", "rb") as f:
    packet = b''
    start = False
    c = 0
    # Skip first 10 bytes to get to the timestamp bytes
    f.read(10)
    # Read the timestamp bytes and convert from bytearray to string
    timestamp = str(f.read(15), 'utf-8')
    # Set the time to the start of the run on the drive day
    timestamp = datetime.datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[9:11]), int(timestamp[11:13]), int(timestamp[13:15]))

    while (byte := f.read(1)):
        if(byte.hex() == '7e'):
            c += 1
            data = parse_packet(packet, variable)
            # print(data['time'])
            timestamp = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
            if (data['name'] != 'Error bytes'):
                # Add time elapsed since the start of the run onto the timestamp (in milliseconds)
                timestamp += datetime.timedelta(microseconds=data['time']*1000)
                # print(timestamp)
            # print(timestamp.isoformat())
            # print(data)
            name = data['name']
            data = data["data"]
            body = [
                    {
                        "measurement": "system",
                        "time": timestamp,
                        "fields": {
                            name: data,
                        }
                    }
                ]
            # wrtr = iw.InfluxWriterTemp()
            # wrtr.write(body)
            time.sleep(0.1)
            packet = b''
            start = True
        elif start:
            packet += byte
    
        # Do stuff with byte.
    print(c)
