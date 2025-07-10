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
    fight_date_form=request.POST.get('fight_date_form')
    dico_4_template = {}
    dico_4_template["fighter_blue"] = return_all_fighters(blue_surname,blue_name)
    dico_4_template["fighter_red"]  = return_all_fighters(red_surname,red_name)
    diff_combats = abs(dico_4_template["fighter_blue"]["nbr_combats_pro"] - dico_4_template["fighter_red"]["nbr_combats_pro"])
    voting_categories = ["Heavyweight","Light Heavyweight","Featherweight","Bantamweight","Flyweight","Strawweight"]
    date_to_time = datetime.strptime(fight_date_form, "%Y-%m-%d")
    if date_to_time < dico_4_template["fighter_blue"]["date_for_next_fight"] or date_to_time < dico_4_template["fighter_red"]["date_for_next_fight"]:
        fight_date_issue = "issue"
    else:
        fight_date_issue = "ok"
    dico_4_template["extra"] = {"diff_combats": diff_combats, "voting_categories": voting_categories, "fight_date_form":fight_date_form, "fight_date_issue":fight_date_issue}
    template = loader.get_template('mmc_result.html')
    return HttpResponse(template.render(dico_4_template, request))
