█████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ 
                                                                                    
                                                                                                                                                                                                                                                         
████████ ██████   █████   ██████ ██   ██ ███████ ██ ██████  ███████    ██████  ██   
   ██    ██   ██ ██   ██ ██      ██  ██  ██      ██ ██   ██ ██         ██   ██ ██   
   ██    ██████  ███████ ██      █████   ███████ ██ ██   ██ █████      ██████  ██   
   ██    ██   ██ ██   ██ ██      ██  ██       ██ ██ ██   ██ ██         ██      ██   
   ██    ██   ██ ██   ██  ██████ ██   ██ ███████ ██ ██████  ███████ ██ ██      ██   
                                                                                    
                                                                                                                                                                                                                                                         
█████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ █████ 


Dummy data (rpi system performance data) is sent to 
InfluxDB every 5 seconds, which is read by Grafana and plotted.

current: system -> json -> Line protocol -> grafana
planned: router (XBee Routyboi) -> coordinator (XBee Coordiboi) -> python -> json -> InfluxDB -> Grafana -> gophermotorsports.com

Tested with Python 3.7 on Raspbian
To-do: run on launch with cron daemon
