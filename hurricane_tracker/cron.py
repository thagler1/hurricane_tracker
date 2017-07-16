from tracker.utils.ftpscrape import update_data
from tracker.models import Storm
import os

def noaa_ftp():
    update_data()
    return True
def test():
    x = Storm.objects.all().count()
    file = open(r'testfile.txt', 'w')
    file.write('Hello World')
    file.write("there are %s storms"%(x))
    file.close()