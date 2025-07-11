#!/usr/bin/python3
from tapo_functions import *


####### VARIABLES ##########
prenom = input("Enter firstname: ")
nom = input("Enter name: ")


print("ALL FIGHTERS FOUND")
research_fighters = return_all_fighters(prenom,nom)
print(research_fighters)

print("______________________")
print(  "CLOSEST FIGHTER FOUND : " )
research_closest_fighter = return_closest_fighters(research_fighters,prenom,nom)
print(research_closest_fighter)

