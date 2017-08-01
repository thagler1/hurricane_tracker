from ..models import Storm, Advisory
from django.contrib.gis.geos import LineString, GEOSGeometry

def add_track_init():
    storms = Storm.objects.all()

    for storm in storms:
        try:
            advs = storm.all_advisories()
            coords = LineString([(a.long, a.lat) for a in advs])
            storm.path = coords
            storm.save()
        except:
            print(storm.stormid)

def define_coords():
    advs = Advisory.objects.all()
    for a in advs:

        a.coordinates = GEOSGeometry('POINT(%s %s)' % (a.long, a.lat), srid=4326)
        a.save()

