from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime
from .models import Storm, Advisory, Posts
import json
from django.core.serializers import serialize
from .utils.slack_bot import post_to_slack
from rest_framework import viewsets
from .utils.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.


def update(request):
    #update_data()
    #archive_scrape.update_data()

    active_storm = storm_query.find_active_advisory()
    inactive_storms = Storm.objects.filter(active=False, year=datetime.date.today().year)
    template = loader.get_template('index.html')
    basin_stats = storm_query.basin_activity_stats()
    geojson = serialize('geojson', active_storm,
              geometry_field='path',
              fields=('stormid','year'))
    context ={
        'active_storm': active_storm,
        'inactive_storms': inactive_storms,
        'basin_stats':basin_stats,
        'geojson':geojson
    }


    return HttpResponse(template.render(context, request))


def stormdata(request, stormid):


    storm = Storm.objects.get(stormid=stormid)
    stormgeo = Storm.objects.filter(stormid=stormid)
    advisories = Advisory.objects.filter(stormid=storm).order_by('-id')
    most_recent = Advisory.objects.filter(stormid=storm).order_by('date')[0]
    storm_id_url = stormid[:4].upper()

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    geojson = serialize('geojson', stormgeo,
              geometry_field='path',
              fields=('stormid','year'))

    adv = Storm.objects.get(stormid=stormid).all_advisories()

    x = [a.date for a in adv]
    y = [a.max_sus_wind for a in adv]
    speed_y = [a.speed for a in adv]
    print(speed_y)


    template = loader.get_template('posts.html')


    context ={
        'storm': storm,
        'advisories': advisories,
        'most_recent': most_recent,
        'storm_id_url': storm_id_url,
        'x': json.dumps(x, default=date_handler),
        'y': json.dumps(y),
        'speed_y': json.dumps(speed_y),
        'advisory':adv,
        'geojson':geojson,

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
    p = Posts.objects.get(target='about')
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

def data_viz(request):
    geojson = serialize('geojson', Storm.objects.all(),
              geometry_field='path',
              fields=('stormid','year'))
    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    years = ['2015','2016', '2017']
    count = []
    for year in years:
        year_count = []
        for i, month in enumerate(months):

            stormcount = Advisory.objects.filter(date__month=i+1, date__year=int(year)).distinct('stormid').count()


            year_count.append(stormcount)
        count.append(year_count)
    print(len(count))
    template = loader.get_template('data.html')
    context = {
        'x': json.dumps(months),
        'y':json.dumps(count),
        'geojson':geojson
    }

    return HttpResponse(template.render(context,request))



class EarthQuakeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all seismic events in the database.
    """


    queryset = Storm.objects.all()
    serializer_class = StormSerializer


@api_view()
def stormdata_json(request, stormid):
    '''
    Return storm meaurements
    '''

    queryset = Storm.objects.filter(stormid=stormid)
    serializer = StormSerializer(queryset, many=True)
    return Response(serializer.data)


def dev_test(request):
    #needed to get around cross site origin response. delete when done

    context = {}
    template = loader.get_template('delta_speed_scatterplot.html')

    return HttpResponse(template.render(context, request))


@api_view()
def windspeed(request):
    '''
    API for getting windspeed vs storm speed graph
    '''

    queryset = Advisory.objects.all()
    serializer = SeasonSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def windSpeedDelta(request):
    '''
    change in wind speed(delta_wind) vs change in storm movement speed(delta_speed)
    '''

    storms = Storm.objects.all()
    delta = []
    for storm in storms:
        advs = storm.all_advisories()
        adv_list= [adv for adv in advs]
        count = advs.count()
        for i, adv in enumerate(adv_list):
            if i+1 < count:
                try:
                    speed1 = adv.speed
                    speed2 = adv_list[i+1].speed
                    dspeed = speed2 - speed1
                    print(adv.date)

                    windspeed = adv.max_sus_wind
                    windspeed2 = adv_list[i+1].max_sus_wind
                    dwind = windspeed2 - windspeed

                    delta.append({'delta_speed':dspeed, 'delta_wind':dwind})
                except:
                    pass
    serializers = DeltaSpeedSerializer(delta, many=True)
    return Response(serializers.data)

def threejshw(request):

    template = loader.get_template('threejshw.html')
    context ={

    }
    return HttpResponse(template.render(context, request))


