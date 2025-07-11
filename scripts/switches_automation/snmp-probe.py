#!/usr/bin/python3
from pysnmp.hlapi import SnmpEngine, UsmUserData, usmHMACSHAAuthProtocol, usmAesCfb128Protocol, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
import getpass
import sys
import base64

#############
## GOAL #####
#############
# Test SNMP configuration on cisco switches 
# Result expected is SNMP answer containing the name
# 
# WRITTEN in 2022



#############
## HOW TO ###
#############
# create a text file containing the list of targeted switches
# switch list should be set in a One Column, ex:
# sw-as01
# sw-as02
# ...
# Then run the command :     ./snmp-probe.py text_file_created

user = getpass.getpass("user")
key = getpass.getpass("key")


listequipement = sys.argv[1]
fichier=open(r'{0}'.format(listequipement), 'r')
lecture1 = fichier.readlines()
fichier.close()



def snmp_v3_get_sysname(user, key, target) :
  auth = UsmUserData(
    userName=user,
    authKey=key,
    authProtocol=usmHMACSHAAuthProtocol,
    privKey=key,
    privProtocol=usmAesCfb128Protocol
  )
  iterator = getCmd(
    SnmpEngine(),
    auth,
    UdpTransportTarget((target, 161)),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
  )
  errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
  return (errorIndication, errorStatus, errorIndex)



for device in lecture1 :
    host = device.rstrip()
    print(snmp_v3_get_sysname(user, key, host))

