from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime
from .models import Storm, Advisory, Posts
import json
from django.core.serializers import serialize
from .utils.slack_bot import post_to_slack


# Create your views here.


def update(request):
    #update_data()
    #archive_scrape.update_data()

    active_storm = storm_query.find_active_advisory()
    post_to_slack("someone is viewing the page")

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

