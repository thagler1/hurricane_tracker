from django.shortcuts import render
from .utils.ftpscrape import update_data
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime
from .models import Storm, Advisory
# Create your views here.


def update(request):
    #update_data()

    active_storm = storm_query.find_active_advisory()
    inactive_storms = Storm.objects.filter(active=False)
    template = loader.get_template('index.html')
    basin_stats = storm_query.basin_activity_stats()
    context ={
        'active_storm': active_storm,
        'inactive_storms': inactive_storms,
        'basin_stats':basin_stats
    }


    return HttpResponse(template.render(context, request))


def stormdata(request, stormid):
    #update_data()

    storm = Storm.objects.get(stormid=stormid)
    advisories = Advisory.objects.filter(stormid=storm)
    most_recent = Advisory.objects.filter(stormid=storm).order_by('-id')[0]
    storm_id_url = stormid[:4].upper()
    template = loader.get_template('posts.html')

    context ={
        'storm': storm,
        'advisories': advisories,
        'most_recent': most_recent,
        'storm_id_url': storm_id_url,
    }


    return HttpResponse(template.render(context, request))