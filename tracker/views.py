from django.shortcuts import render, render_to_response
from .utils.ftpscrape import update_data
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .utils import storm_query
import datetime
from .models import Storm, Advisory, Posts
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
# Create your views here.


def update(request):
    update_data()

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

    template = loader.get_template('posts.html')


    context ={
        'storm': storm,
        'advisories': advisories,
        'most_recent': most_recent,
        'storm_id_url': storm_id_url,

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

def data_viz(request, stormid):

    storm = Storm.objects.get(stormid=stormid)
    advisories = Advisory.objects.filter(stormid=storm).order_by('-id')

    #Plot intensity
    x = [i for i, x in enumerate(advisories)]
    y = [adv.max_sus_wind for adv in advisories]
    print(y)
    title = 'y = f(x)'

    plot = figure(title=title,
                  x_axis_label='X-Axis',
                  y_axis_label='Y-Axis',
                  plot_width=400,
                  plot_height=400)
    plot.line(x, y, legend='f(x)', line_width=2)
    # Store components
    script, div = components(plot)

    # Feed them to the Django template.
    return render_to_response('data_viz.html',
                              {'script': script, 'div': div})