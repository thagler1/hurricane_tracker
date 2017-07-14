from ..models import Storm, Advisory
import datetime
import operator


def find_active_advisory():
    offset = datetime.datetime.now() + datetime.timedelta(hours=-12)
    now = datetime.datetime.now()
    recent_advisories = Advisory.objects.filter(date__range=(offset, now))
    storm = {}
    for adv in recent_advisories:
        storm.setdefault(adv.stormid, [])
        storm[adv.stormid].append(adv)
        s = Storm.objects.get(stormid = adv.stormid)
        s.active = True
        s.save()
    all_storms = Storm.objects.filter(active=True)

    #itereate through all active storms then deactivate ones that do not have advisories
    for event in all_storms:
        if event not in storm:
            event.active = False
            event.save()

    return all_storms


def basin_activity_stats():
    '''
    
    :return:{'basin':count, etc} 
    '''

    def get_basin_name(basin):
        b = Storm.basins
        name = [value for key,value in b if key == basin.upper()]
        return name[0]


    all_basins = Storm.objects.values('region').distinct()




    r = {}
    for basin in all_basins:
        count = Storm.objects.filter(region=basin['region']).count()
        name = get_basin_name(basin['region'])
        r.setdefault(name,count)

    return r