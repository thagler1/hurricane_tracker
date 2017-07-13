from django.shortcuts import render
from .utils.ftpscrape import update_data
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime

# Create your views here.
def update(request):
    update_data()

    active_storm = storm_query.find_active_advisory()
    template = loader.get_template('index.html')
    context ={
        'active_storm': active_storm
    }


    return HttpResponse(template.render(context, request))
