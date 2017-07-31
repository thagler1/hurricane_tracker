from ..models import Storm, Advisory
from django.contrib.gis.geos import LineString

def add_track_init():
    storms = Storm.objects.filter(path=None)
    for storm in storms:
        advs = Advisory.objects.filter(stormid=storm).order_by('date')
        for a in advs:
            if storm.path:
                storm.path.append((a.lat,a.long))
            else:
                storm.path =LineString((a.lat,a.long))

        print(storm.path)
        storm.save()