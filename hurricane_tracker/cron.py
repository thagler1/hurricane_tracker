from tracker.utils.ftpscrape import update_data
from tracker.models import Storm
import os

def noaa_ftp():
    update_data()
    print("complete")
    return True


def test():
    print("Hello")
    return 0
