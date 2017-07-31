from ..models import Storm, Advisory

def add_track_init():
    storms = Storm.objects.filter(path=None)
    for storm in storms:
        advs = Advisory.objects.filter(stormid=storm.storm_id).order_by('date')
        path = [(a.lat, a.long) for a in advs]
        storm.path = path
        print(path)
        storm.save()
