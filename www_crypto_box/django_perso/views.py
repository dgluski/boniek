from django.http import HttpResponse
from django.template import loader
from functions import *
from dico_pass import *

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def keepass_menu(request):
  dico_transport = {"contenu":dico}
  template = loader.get_template('keepass_menu.html')
  return HttpResponse(template.render(dico_transport, request))

def keepass_result(request) :
    klusz=request.POST.get('klusz')
    entry=request.POST.get('entry')
    dico_answer = return_pass(klusz,entry,dico)
    template = loader.get_template('keepass_result.html')
    return HttpResponse(template.render(dico_answer, request))

def algopass_menu(request):
  template = loader.get_template('algopass_menu.html')
  return HttpResponse(template.render())

def algopass_result(request) :
    klusz=request.POST.get('klusz')
    variable_1=request.POST.get('variable_1')
    variable_2=request.POST.get('variable_2')
    dico_answer = return_algo_pass(klusz,variable_1,variable_2)
    template = loader.get_template('algopass_result.html')
    return HttpResponse(template.render(dico_answer, request))

