from django.shortcuts import render
from functions import *
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def get_answer(request):
  answer=request.POST.get('answer')
  result = check_answer(answer)
  template = loader.get_template('answer.html')
  return HttpResponse(template.render(result,request))
