from ..models import Storm, Advisory

def add_track_init():
    storms = Storm.objects.filter(path=None)
    for storm in storms:
        advs = Advisory.objects.filter(stormid=storm).order_by('date')
        for a in advs:
            storm.path.append((a.lat,a.long))

        print(storm.path)
        storm.save()