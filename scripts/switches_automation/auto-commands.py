#!/usr/bin/python3.9

# Commong import

from sw_functions import *

from netmiko import ConnectHandler
import sys
import select
import paramiko
import linecache
import os.path
import getpass
import os
import datetime
import multiprocessing
import time
from getpass import getpass
import logging


#############
## GOAL #####
#############
# Run several commands on multiples switches in parallel
# Result is a HTML formatted file
# Scope is CISCO devices
# WRITTEN in 2024



#############
## HOW TO ###
#############
# create a text file containing the list of targeted switches                    
# switch list should be set in a One Column, ex:
# sw-as01
# sw-as02
# ...
# Then run the command :     ./auto-commands.py text_file_created



#get the identity
adm_username = input("Admin login:")
adm_password = getpass(prompt = 'Input the Password:')
# get inventory list
current_time = datetime.datetime.now()

listequipement = sys.argv[1]
fichier=open(r'{0}'.format(listequipement), 'r')
lecture1 = fichier.readlines()
fichier.close()

liste_wish = []

for device in lecture1 :
    liste_wish.append({"sw_username":adm_username, "sw_password":adm_password,"hostname":device,"os":"cisco_ios"})


f = open(f'/tmp/snapshot-{current_time}.php', 'w')
f.close


def execute(dico):
        hostname = dico["hostname"].rstrip().lower()
        sw_username = dico["sw_username"]
        sw_password = dico["sw_password"]
        platform = dico["os"]
        print("------CONNECTING DEVICE :"+hostname+"-----------------<br>", file=f)
        try:
                device = ConnectHandler(device_type=platform, ip=hostname, username=sw_username, password=sw_password)
                # SHOW command example : display the version of the device
                commands = ["show log", "show mac address-table","show spanning-tree details","show ip arp",
                            "show ip ospf neighbor","show ip ospf database","show ip route",
                            "show ip bgp su","show ip bgp"]
                for command in commands:
                    output = device.send_command(command, strip_command=False, strip_prompt=False, read_timeout=60)
                    if output :
                      for idx, line in enumerate(output.splitlines()) :
                          print(f"<font color='grey'>{hostname}#</font><font color='green'> {line}</font><br>", file=f)

#                command = ["interface vlan 316","ip dhcp relay address 10.127.10.11", "no ip dhcp relay address 10.0.3.59"]
#                output = device.send_config_set(command, read_timeout=60)
#                print(output)
                device.disconnect()
                status = "connection established and commands pushed"
                status_color = "green"
        except Exception as e:
            print(f"---> SW: {hostname} <---- ISSUE : {e.args} <br>", file=f)
            status = "connection failed"
            status_color = "red"
        return({"hostname":hostname, "status":status, "status_color":status_color})

# Launch the job


a_pool = multiprocessing.Pool()
result = a_pool.map(execute, liste_wish)
a_pool.close()
a_pool.join()

print("--------END OF WORK-----------\n", file=f)
print("--------SUMMARY-----------", file=f)
for dico in result:
    print(f"<font color='{dico['status_color']}'>{dico['status']}-------------{dico['hostname']}</font><br>", file=f)

f.close()

