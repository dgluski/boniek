#!/usr/bin/python3
from urllib.request import urlopen
from difflib import SequenceMatcher
import time
import re
from datetime import datetime, date, timedelta
import requests

def clean_name(name):
    name = name.rstrip()
    name = name.lstrip()
    name = name.replace(" ","-")
    return(name)

def clean_and_count_palmares(string):
    palmares_counted = {"type":"","total":"", "elite":""}
    re_palmares = re.compile(r'^(A?m?) ?(\d*)-(\d*)-(\d*),? ?(\d*) ?(N?C?)$')
    m = re.match(re_palmares, string)
    if m.group(1) :
        palmares_counted["type"] = "Amateur"
    else:
        palmares_counted["type"] = "Professionel"
    count = 0
    i = 2
    while m.group(i) and i != 6 :
        count = count + int(m.group(i))
        i = i + 1
    palmares_counted["total"] = count
    if count > 9 and palmares_counted["type"] == "Professionel":
        palmares_counted["elite"] = "elite 1"
    elif count < 10 and palmares_counted["type"] == "Professionel":
        palmares_counted["elite"] = "elite 2"
    elif count > 5 and palmares_counted["type"] == "Amateur":
        palmares_counted["elite"] = "elite 2"
    elif count < 6 and palmares_counted["type"] == "Amateur":
        palmares_counted["elite"] = "non eligible"
    return(palmares_counted)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_names(string) :
  if "&quot;" in string:
    full_name_1 = string.split('">')[1]
    full_name_2 = full_name_1.split("<")[0]
    full_name_3_surname = full_name_2.split("&quot;")[0].rstrip()
    full_name_3_name = full_name_2.split("&quot;")[2].lstrip()
  else:
    full_name_1 = string.split('">')[1]
    full_name_2 = full_name_1.split("<")[0]
    if len(full_name_2.split()) > 1 :
      full_name_3_surname = ""
      for part in full_name_2.split()[:-1]:
        full_name_3_surname = full_name_3_surname+part
      full_name_3_name = full_name_2.split()[-1]
    else:
      full_name_3_surname = ""
      full_name_3_name = full_name_2.split()[0]
  return([full_name_3_name,full_name_3_surname])

def return_all_fighters(prenom,nom) :

  url_tapology_search = "https://www.tapology.com/search?term="
  dico_fighters= {}
  prenom = clean_name(prenom)
  nom = clean_name(nom)
  page = urlopen(f"{url_tapology_search}{prenom}+{nom}")
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")
  if "/fightcenter/fighters/" not in html:
      dico_fighters["name"] = nom
      dico_fighters["surname"] = prenom
      dico_fighters["categorie"] = "non trouve sur tapology"
      dico_fighters["palmares"] = "non trouve sur tapology"
      dico_fighters["nbr_combats"] = 0
      dico_fighters["type"] = "indetermine"
      dico_fighters["elite"] = "elite 2"
      return(dico_fighters)

  html_line = html.splitlines()
  for idx, line in enumerate(html_line):
  # Check if beginning
    if "/fightcenter/fighters/" in line :
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]] = {}
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["name"] = find_names(line)[0]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["surname"] = find_names(line)[1]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["categorie"] = html_line[idx+2].split(">")[1].split("<")[0]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["palmares"] = html_line[idx+4].split(">")[1].split("<")[0]
      palmares = html_line[idx+4].split(">")[1].split("<")[0]
      palmares_counted = clean_and_count_palmares(palmares)
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["nbr_combats"] = palmares_counted["total"]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["type"] = palmares_counted["type"]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["elite"] = palmares_counted["elite"]
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["link_to_details"] = line.split('"')[1]
  closest_fighter = return_closest_fighters(dico_fighters,prenom,nom)
  dico_with_details = retreive_details(closest_fighter["link_to_details"])
  closest_fighter.update(dico_with_details)
  return(closest_fighter)

def return_closest_fighters(dico_fighters,prenom,nom) :
  closest_fighter = {
                   "match_percent_name":0
                  }
  for key,value in dico_fighters.items():
    value["match_percent_name"] = int(similar(f"{prenom} {nom}",f"{value['surname']} {value['name']}")*100)
    if value["match_percent_name"] > closest_fighter["match_percent_name"]:
      closest_fighter = value
  return(closest_fighter)

def return_all_fighters_from_list(list_word):
  final_dico_fighters = {}
  for idx, word in enumerate(list_word) :
      print(word, idx,"/",len(list_word))
      final_dico_fighters.update(return_all_fighters(word,""))
      time.sleep(30)
  return(final_dico_fighters)

def retreive_details(link):
  url_tapology_search2 = "https://www.tapology.com"+link
  dico_fighter_details = {}
  dico_fighter_details["last_fight_result"] = "unknown"
  dico_fighter_details["list_of_KO_date"] = []
  headers = {'User-Agent': 'PostmanRuntime/7.29.2'}
  response = requests.request("GET", url_tapology_search2, headers=headers, data={})
  html_text = response.text
  html_line2 = html_text.splitlines()
  for idx2, line2 in enumerate(html_line2):
    if "Last Fight:" in line2 :
      time_in_string = html_line2[idx2+1].split(">")[1].split("<")[0]
      if time_in_string != "N/A" :
        time_in_date = datetime.strptime(time_in_string, "%B %d, %Y")
      else :
        time_in_date = datetime.strptime("January,01,0000", "%B,%d,%Y")
      dico_fighter_details["last_fight_date"] = time_in_date
  # Check if beginning
    if "<li data-bout-id" in line2 :
      i = 1
      full_result = ""
      simple_result = line2.split("data-status='")[1].split("'")[0]
      while "</li>" not in html_line2[idx2+i] :
          # Take the date
          if "<div class='date'>" in html_line2[idx2+i] :
              time_in_string_candidate = html_line2[idx2+i+1].rstrip()
              if time_in_string_candidate != "N/A" :
                 time_in_date_candidate = datetime.strptime(time_in_string_candidate, "%Y.%m.%d")
              else :
                 time_in_date_candidate = datetime.strptime(time_in_string, "%B %d, %Y")
          # register if full fight is present
          if "Bout Page" in html_line2[idx2+i] :
              full_result = html_line2[idx2+i].split(">")[1].split("<")[0]
          i=i+1
      # register in KOTKO List
      if "Loss" in simple_result and "KO/TKO" in full_result   :
          dico_fighter_details["list_of_KO_date"].append(time_in_date_candidate)
      
      # register is match the last match date
      if time_in_date_candidate == dico_fighter_details["last_fight_date"] :
        dico_fighter_details["last_fight_result"] = f"{simple_result} {full_result}"
  if "KO/TKO" in dico_fighter_details["last_fight_result"] and "Loss" in dico_fighter_details["last_fight_result"] :
      dico_fighter_details["date_for_next_fight"] = dico_fighter_details["last_fight_date"] + timedelta(days=28)
  else :
      dico_fighter_details["date_for_next_fight"] = dico_fighter_details["last_fight_date"] + timedelta(days=21)
  return(dico_fighter_details)


