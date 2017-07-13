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
    return storm

