<div align="center">

  <img src="./img/logo.png" width="200px">
  <h1>Telemetry</h1>
</div>


<p align="center">
   Trackside telemetry system for <a href="https://gophermotorsports.com">Gopher Motorsports</a>
</p>


## Features

* Data streaming over XBee radio transmitters
* Database storage and visualisation
* Built-in vehicle sensor simulator

## Description
The intended use of this package is for drive days and competition for Gopher Motorsports - UMN FSAE. One [XBee](https://www.digi.com/xbee) radio transmitter is connected to the DLM within the vehicle. Data packets containing sensor information about the car is streamed to another XBee connected to a trackside computer. This package will parse the incoming bytes, store the data in [InfluxDB](https://www.influxdata.com/), and display the data in [Grafana](https://grafana.com/).


## Installation
Please install using this command
```{bash}
curl -LJO https://github.com/gopher-motorsports/trackside-telemetry/releases/download/cli/trackside-0.9.1-py3-none-any.whl ; pip install trackside-0.9.1-py3-none-any.whl
```

## Usage

### Trackside
[reciever.py](trackside/reciever.py) processes a packet sent to the USB-connected XBee
> **Note:** `--usb` flag may need to be used depending on the name of your USB port in /dev. Example usage:
```{bash}
$ python reciever.py --usb /dev/ttyUSB1
```

### Simulation
[sender.py](trackside/sender.py) sends a packet to a USB-connected XBee


### Python Usage 
```{python}
import trackside as ts
```
When the package is imported, the reciever begins. To force it, call
```{python}
ts.reciever()
```

To start and run the DLMSimulator, and decode a test packet:
```{python}
sim = ts.DLM()
sim.run()
packet = sim.data
output = parse_packet(packet)
``` 

To log a CSV file in InfluxDB:
```{python}
iw = ts.InfluxWriter()
iw.write_csv('./file.csv')
```

To read a packet waiting in the XBee buffer:
```{python}
tl = ts.TracksideLogger()
bytes = tl.read()
output = parse_packet(bytes)
del tl
```


## Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/inessadl/readme/issues)

Organizers
- [Henry O'Callaghan](https://github.com/hocally)
- [Nirbhay Vig](https://github.com/nirbhayvig)

Developers
- [Anton King](https://github.com/antonsking)
- [Sriram Nutulapati](https://github.com/Sriram212)
- [Erick Ti](https://github.com/erick-ti)

## Demo
Please watch our [video demo.](https://www.youtube.com/watch?v=CE0avbeNgHw)


