#!/usr/bin/python3


from netmiko import ConnectHandler
import sys
import time
import select
import paramiko
import re
import linecache
import re
import os.path
import getpass
#from linecache_data import *



#############
## GOAL #####
#############
# set the description of cisco switches interfaces based on cdp neighbors
# update is doing in live 
# Scope is CISCO devices
# WRITTEN in 2019


#############
## HOW TO ###
#############
# create a text file containing the list of targeted switches
# switch list should be set in a One Column, ex:
# sw-as01
# sw-as02
# ...
# Then run the command :     ./auto-description.py text_file_created


username = input("login :")
password = getpass.getpass("password :")

re_interface = re.compile(r'^[^ ]+\s+([^,]+).+[\r\n]*$')
re_neighbor = re.compile(r'^[^:]+:\s*([^ .]+)[^\r\n]*[\r\n]*$')
re_po = re.compile(r'^\s+[^ ]+\s([0-9]+).*[\r\n]*$')


# Consultation du fichier contenant les equipements

listequipement = sys.argv[1]
fichier=open(r'{0}'.format(listequipement), 'r')
lecture1 = fichier.readlines()
fichier.close()


for line in lecture1:
        hostname = line.rstrip()
        print('---------EQUIPMENT EN COURS DE MOFIFICATION :'+hostname+'-----------')
        # Recuperation des neighbor Cdp
        fd = open(r'/var/tmp/neighbor-list.txt','w')
        old_stdout = sys.stdout
        sys.stdout = fd
        platform = 'cisco_nxos'
        try :
                device = ConnectHandler(device_type=platform, ip=hostname, username=username, password=password)
                output = device.send_command('sh cdp neighbor detail | i Device')
                print(output)

                fd.close()

                # Recuperation des interfaces correspondantes
                fd = open(r'/var/tmp/interface-list.txt','w')
                sys.stdout = fd


                output = device.send_command('sh cdp neighbor detail | i Interface:')
                print(output)
                fd.close()

                sys.stdout = old_stdout

                # Compte le nombre de ligne
                fic=open('/var/tmp/interface-list.txt', 'r')
                lecture = fic.readlines()
                N_lignes = len(lecture)
                fic.close()

                for x in range(N_lignes):
                        interface1 = linecache.getline('/var/tmp/interface-list.txt', x+1)
                        m=re.match(re_interface, interface1)
                        interface2=m.group(1)
                        print("Nom de l interface:"+interface2)
                        neighbor1 = linecache.getline('/var/tmp/neighbor-list.txt', x+1)
                        m=re.match(re_neighbor, neighbor1)
                        neighbor2=m.group(1).replace('\n','')
                        print("Nom du Voisin CDP:"+neighbor2)
                        if hostname[0:3] == neighbor2[0:3]:

                           config_commands = ['interface '+interface2, 'description '+neighbor2+'-UPK']
                           output = device.send_config_set(config_commands, delay_factor=15)
                           print(output)
                           #Configuration du po
                           numero_po1 = device.send_command('show run int '+interface2+' | i channel')
                           print(numero_po1)
                           m=re.match(re_po, numero_po1)
                           print(m)
                           if m is not None:
                                numero_po2=m.group(1)
                                print("Numero de Po: "+numero_po2)
                                config_commands = ['interface Port-channel '+numero_po2, 'description '+neighbor2+'-UPK']
                                output = device.send_config_set(config_commands, delay_factor=15)
                                print(output)

                output = device.send_command_expect('write memory')
                linecache.clearcache()
                os.remove('/var/tmp/interface-list.txt')
                os.remove('/var/tmp/neighbor-list.txt')
                device.disconnect()
        except :
                print('device unreachable')

