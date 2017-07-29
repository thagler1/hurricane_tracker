from django.shortcuts import render, render_to_response
from .utils.ftpscrape import update_data
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime
from .models import Storm, Advisory, Posts
import json

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
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


    storm = Storm.objects.get(stormid=stormid)
    advisories = Advisory.objects.filter(stormid=storm).order_by('-id')
    most_recent = Advisory.objects.filter(stormid=storm).order_by('date')[0]
    storm_id_url = stormid[:4].upper()

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    adv = Storm.objects.get(stormid=stormid).all_advisories()

    x = [a.date for a in adv]
    y = [a.max_sus_wind for a in adv]


    template = loader.get_template('posts.html')


    context ={
        'storm': storm,
        'advisories': advisories,
        'most_recent': most_recent,
        'storm_id_url': storm_id_url,
        'x': json.dumps(x, default=date_handler),
        'y': json.dumps(y)

    }


    return HttpResponse(template.render(context, request))

def advisory(request, advisory_id):
    adv = Advisory.objects.get(advisory_id=advisory_id)


    context ={
        'adv': adv,
    }
    template = loader.get_template('advisory.html')

    return HttpResponse(template.render(context, request))

def about(request):
    p = Posts.objects.get(title='About Tropical Storm Tracker')
    context ={
        'post':p
    }
    template = loader.get_template('about.html')

    return HttpResponse(template.render(context, request))


def stormviz(request, stormid):
    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    adv = Storm.objects.get(stormid=stormid).all_advisories()

    x = [a.date for a in adv]
    y = [a.max_sus_wind for a in adv]
    template = loader.get_template('data_viz.html')
    context ={
        'x':json.dumps(x, default=date_handler),
        'y': json.dumps(y)
    }
    return HttpResponse(template.render(context, request))
