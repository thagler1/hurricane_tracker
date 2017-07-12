from django.shortcuts import render
from .utils.ftpscrape import update_data
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

# Create your views here.
def update(request):
    #update_data()
    template = loader.get_template('index.html')
    context ={}
    return HttpResponse(template.render(context, request))
