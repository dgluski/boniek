#!/usr/bin/python3
from tapo_functions import *
from itertools import permutations
import numpy as np
import sys


list_letter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

possible_words_1 = list(permutations(list_letter, 3))
possible_words_2 = []


for word in possible_words_1 :
  possible_words_2.append("".join(word))

list_of_list = np.array_split(possible_words_2, 33)
#print("5-the 7 groups of switches created")


for idx, liste in enumerate(list_of_list) :
  test_search = return_all_fighters_from_list(liste)
  f = open("/home/zbigniew/bis_test_search.part."+str(idx), 'w+')
  print(test_search, file=f)
  f.close
  time.sleep(3600)
