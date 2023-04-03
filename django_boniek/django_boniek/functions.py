#!/usr/bin/python3
from urllib.request import urlopen
from difflib import SequenceMatcher
import time



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
  page = urlopen(f"{url_tapology_search}{prenom}+{nom}")
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")
  if "/fightcenter/fighters/" not in html:
      dico_fighters["name"] = nom
      dico_fighters["surname"] = prenom
      dico_fighters["categorie"] = "non trouve sur tapology"
      dico_fighters["palmares"] = "non trouve sur tapology"
      dico_fighters["nbr_combats"] = 0
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
      if "Am" in palmares:
          dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["nbr_combats"] = 0
          dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["elite"] = "elite 2"
          continue
      nbr_combats = 0
      for number in palmares.split("-") : 
          nbr_combats = nbr_combats + int(number)
      dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["nbr_combats"] = nbr_combats
      if nbr_combats > 9 :
          dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["elite"] = "elite 1"
      else :
          dico_fighters["fighter"+find_names(line)[0]+find_names(line)[1]]["elite"] = "elite 2"
  closest_fighter = return_closest_fighters(dico_fighters,prenom,nom)
  return(closest_fighter)

def return_closest_fighters(dico_fighters,prenom,nom) :
  closest_fighter = {
                   "match_percent_name":0
                  }
  for key,value in dico_fighters.items():
    value["match_percent_name"] = similar(f"{prenom} {nom}",f"{value['surname']} {value['name']}")*100
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

