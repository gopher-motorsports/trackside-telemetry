
import yaml

filepath = "./go4-22c.yaml"
#global variable
file_descriptor = open(filepath, "r")  
data = yaml.load(file_descriptor, yaml.FullLoader)
sensors = data['parameters']

fp = open("sensor_ids.txt","w+")

for i,sen in enumerate(sensors):
    fp.write(f"{sen} {i}\n")

fp.close()

'''
import re
import subprocess



device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []
for i in df.split(b'\n'):
    if i:
        info = device_re.match(i)
        if info:
            dinfo = info.groupdict()
            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            devices.append(dinfo)
            
print(devices)
'''