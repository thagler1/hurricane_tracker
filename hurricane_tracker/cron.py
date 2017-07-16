from tracker.utils.ftpscrape import update_data
from tracker.models import Storm

def noaa_ftp():
    update_data()
    return True
def test():
    x = Storm.objects.all().count()
    print("there are %s storms"%(x))