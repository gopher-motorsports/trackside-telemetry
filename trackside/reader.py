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
    while (byte := f.read(1)):
        if(byte.hex() == '7e'):
            c += 1
            data = parse_packet(packet, variable)
            name = data['name']
            data = data["data"]
            timestamp = datetime.datetime.utcnow().isoformat()
            body = [
                    {
                        "measurement": "system",
                        "time": timestamp,
                        "fields": {
                            name: data,
                        }
                    }
                ]
            wrtr = iw.InfluxWriterTemp()
            wrtr.write(body)
            time.sleep(0.1)
            packet = b''
            start = True
        elif start:
            packet += byte
    
        # Do stuff with byte.
    print(c)
