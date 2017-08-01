from ..models import Storm, Advisory
from django.contrib.gis.geos import LineString

def add_track_init():
    storms = Storm.objects.all()

    for storm in storms:
        try:
            advs = storm.get_advisories()
            coords = LineString([(a.long, a.lat) for a in advs])
            storm.path = coords
            storm.save()
        except:
            print(storm.stormid)

