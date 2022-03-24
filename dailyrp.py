#!/usr/bin/env python3
from netmiko import ConnectHandler
import netmiko
from datetime import datetime
Router1= {
            'device_type': 'cisco_ios',
            'ip': '192.168.177.10',
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
            'verbose': False,
            }
Router2= {
            'device_type': 'cisco_ios',
            'ip': '192.168.177.20',
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
            'verbose': False,
            }
all_routers=[Router1,Router2]
## create filename with date-month-year
current_time=datetime.now()
current_date=current_time.strftime("%d")
current_month=current_time.strftime("%m")
current_year=current_time.strftime("%Y")
#login to each router
for routers in all_routers:
    net_connect=ConnectHandler(**routers)
    net_connect.enable()
    ##Get hostname router
    get_hostname_router="show running-config | include hostname"
    GetHostName_command = net_connect.send_command_timing(get_hostname_router)
    hostname_router=GetHostName_command.split(" ")[1]
    ##set name for backup file
    filename=hostname_router+"_"+current_date+"_"+current_month+"_"+current_year
    #show run and store in file
    running_cfg=net_connect.send_command_timing("show running-config")
    f=open(filename,'w')
    f.write(running_cfg)