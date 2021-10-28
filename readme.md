# Trackside Telemetry Software

## Trackside module for realtime vehicle telemetry
## Gopher Motorsports 2021



Old readme:

PI_CLI_App can be executed through:
$ssh pi@<ipaddress> 
$cd <repo-folder> 
$./PI_CLI_App
if
1. The PI is on
2. The Router XBee (Routyboi) is connected to USB1 (bottom right USB port)
Since its not running on your machine, there ***are no dependencies***.

Streamer (testing script) can be executed on a computer with the Coordinator XBee
$cd <repo-folder> 
$./Streamer
if it is also connected to USB1. May need to edit the 
port variable if its connected to if connected to incorrect USB port. 
Dependencies for streamer are:
Python 3.7+
pip install:
  -psutil
  -datetime
  -serial
