#!/usr/bin/python3
from urllib.request import urlopen
from difflib import SequenceMatcher
import time
import re
from datetime import datetime, date, timedelta
import requests
import base64



def check_answer(response):
    if response.lower() == "mortal kombat":
        result = 1
    else :
        result = 0
    return result
