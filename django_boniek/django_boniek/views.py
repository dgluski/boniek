from django.http import HttpResponse
from django.template import loader
from functions import *

def index(request):
    return HttpResponse("Ca marche 2")


def mmc_form(request):
  template = loader.get_template('mmc_form.html')
  return HttpResponse(template.render())

def mmc_result(request) :
    blue_surname=request.POST.get('blue_surname')
    blue_name=request.POST.get('blue_name')
    red_surname=request.POST.get('red_surname')
    red_name=request.POST.get('red_name')
    dico_4_template = {}
    dico_4_template["fighter_blue"] = return_all_fighters(blue_surname,blue_name)
    dico_4_template["fighter_red"]  = return_all_fighters(red_surname,red_name)
    diff_combats = abs(dico_4_template["fighter_blue"]["nbr_combats"] - dico_4_template["fighter_red"]["nbr_combats"])
    voting_categories = ["Heavyweight","Light Heavyweight","Featherweight","Bantamweight","Flyweight","Strawweight"]
    dico_4_template["extra"] = {"diff_combats": diff_combats, "voting_categories": voting_categories}
    template = loader.get_template('mmc_result.html')
    return HttpResponse(template.render(dico_4_template, request))
