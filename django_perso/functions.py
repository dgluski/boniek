#!/usr/bin/python3
from urllib.request import urlopen
from difflib import SequenceMatcher
import time
import re
from datetime import datetime, date, timedelta
import requests
import base64
from cryptography.fernet import Fernet
from dico_pass import *


def return_pass(klusz, entry, dico) :
   klusz = f'{klusz}00'
   klusz_bytes = klusz.encode("ascii")
   klusz_bytes_base64 = base64.b64encode(klusz_bytes)
   f = Fernet(klusz_bytes_base64)
   dico_answer = { "password": f.decrypt(dico[entry]["password"]) }
   return dico_answer

def return_algo_pass(klusz,variable_1,variable_2) :

    dico_answer = { "password": klusz+variable_1+variable_2}
    return dico_answer
