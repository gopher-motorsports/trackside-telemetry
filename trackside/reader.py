from utils import *
import time
import InfluxWriterTemp as iw

here = str(pathlib.Path(__file__).absolute())
filepath = here[:-10] + os.path.join("\\data","go4-22c.yaml")
#global variable
file_descriptor = open(filepath, "r")  
variable = yaml.load(file_descriptor, yaml.FullLoader)

for yearFolder in os.listdir("data"):
    yearPath = os.path.join("data", yearFolder)
    if os.path.isdir(yearPath):
        print(yearPath)
        for dayFolder in os.listdir(yearPath):
            dayPath = os.path.join(yearPath, dayFolder)
            if os.path.isdir(dayPath):
                print(dayPath)
                for gdatFile in os.listdir(dayPath):
                    gdatPath = os.path.join(dayPath, gdatFile)
                    if os.path.isfile(gdatPath):
                        print(gdatPath)
                        # with open("dlm_data_20210413_004735.gdat", "rb") as f:
                        with open(gdatPath, "rb") as f:
                            packet = b''
                            start = False
                            c = 0
                            # Get the date from the folder name
                            date = gdatPath[20:28]
                            # print(date)
                            # Skip first 19 bytes to get to hours, minutes, and seconds bytes
                            f.read(19)
                            # Read the hours, minutes, and seconds bytes and convert from bytearray to string
                            timestamp = str(f.read(6), 'utf-8')
                            # Set the time to the start of the run on the drive day
                            initTimestamp = datetime.datetime(int("20" + date[6:8]), int(date[:2]), int(date[3:5]), int(timestamp[:2]), int(timestamp[2:4]), int(timestamp[4:6]))
                            print(initTimestamp.isoformat())

                            while (byte := f.read(1)):
                                if(byte.hex() == '7e'):
                                    c += 1
                                    data = parse_packet(packet, variable)
                                    # print(data)
                                    # print(data['time'])
                                    currTimestamp = datetime.datetime(initTimestamp.year, initTimestamp.month, initTimestamp.day, initTimestamp.hour, initTimestamp.minute, initTimestamp.second)
                                    if (data['name'] != 'Error bytes'):
                                        # Add time elapsed since the start of the run onto the timestamp (in milliseconds)
                                        # print("add: " + str(data['time']/1000))
                                        currTimestamp = initTimestamp + datetime.timedelta(microseconds=data['time']*1000)
                                        print(currTimestamp.isoformat())
                                    # print(data)
                                    name = data['name']
                                    data = data["data"]
                                    body = [
                                            {
                                                "measurement": "system",
                                                "time": currTimestamp,
                                                "fields": {
                                                    name: data,
                                                }
                                            }
                                        ]
                                    wrtr = iw.InfluxWriterTemp()
                                    wrtr.write(body)
                                    time.sleep(0.01)
                                    packet = b''
                                    start = True
                                elif start:
                                    packet += byte
                            
                                # Do stuff with byte.
                            print(c)
