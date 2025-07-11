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
# Apply a bandwidth value on SVI ospf interfaces in order to reflect reality
# 
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
# Then run the command :     ./auto-svi-ospf-bw.py text_file_created



username = input("login :")
password = getpass.getpass("password :")


re_vlan = re.compile(r'^.+([V][l]([a-z]+|)([0-9]+))(.+|)$')
re_ip = re.compile(r'^[ ]?(\d+[.]\d+[.]\d+[.]\d+)(.+)[ ](\d+[.]\d+[.]\d+[.]\d+)(.+|)$')
re_mac = re.compile(r'^.+[ ](([a-f]|[0-9]){4}[.]([a-f]|[0-9]){4}[.]([a-f]|[0-9]){4})[ ].+$')
re_bandwith = re.compile(r'^.+([B][W])(.+)[K]+.+$')


# Consultation du fichier contenant les equipements

listequipement = sys.argv[1]
fichier=open(r'{0}'.format(listequipement), 'r')
lecture1 = fichier.readlines()
fichier.close()

for line in lecture1:
        hostname = line.rstrip()
        print('---------EQUIPMENT EN COURS DE MOFIFICATION :'+hostname+'-----------')
        # Recuperation des neighbor OSPF
        platform = 'cisco_nxos'
        try :
                device = ConnectHandler(device_type=platform, ip=hostname, username=username, password=password)
                output = device.send_command('show ip ospf neighbor | i Vl')
                print(output)
                if output :
                        for ligne in output.splitlines() :
                                m=re.match(re_vlan, ligne)
                                vlan_re=m.group(3)
#                               print(vlan_re)
                                int_vlan_re=m.group(1)
#                               print(int_vlan_re)
                                n=re.match(re_ip, ligne)
                                ip_re=n.group(3)
#                               print(ip_re)
                                output = device.send_command('show ip arp '+ip_re+' | i 10.')
                                print(output)
                                if output :
                                        for ligne in output.splitlines() :
                                                o=re.match(re_mac, ligne)
                                                mac=o.group(1)
#                                               print(mac)
                                                output = device.send_command('show mac address-table address '+mac+' | i '+vlan_re)
#                                               print(output)
                                                if output :
                                                        for ligne in output.splitlines() :
                                                                interfacename = ligne.split()[-1]
                                                                output = device.send_command('show interface '+interfacename+' | i BW')
                                                                print(output)
                                                                if output :
                                                                        for ligne in output.splitlines():
                                                                                p=re.match(re_bandwith, ligne)
                                                                                bandwith=p.group(2)
                                                                                print(bandwith)
                                                                                #Configuration de la bande passante
                                                                                config_commands = ['interface  '+int_vlan_re, 'bandwidth'+bandwith]
                                                                                output = device.send_config_set(config_commands)
                                                                                print(output)
                                                                else :
                                                                        print("pas de bande passante correcte "+hostname)
                                                else :
                                                        print("pas de interface associe pour "+hostname)
                                else :
                                        print("pas de mac associe pour "+hostname)
                else :
                        print("pas de neighbor OSPF pour "+hostname)
        except paramiko.AuthenticationException:
                print("Authentication failed, please verify your credentials: %s")
        except paramiko.SSHException as sshException:
                print("Unable to establish SSH connection: %s" % sshException)
        except paramiko.BadHostKeyException as badHostKeyException:
                print("Unable to verify server's host key: %s" % badHostKeyException)
        except Exception as e:
                print(e.args)

