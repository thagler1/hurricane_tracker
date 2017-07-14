from django.db import models
from django.utils.deconstruct import deconstructible
import base64
import os
import PIL


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        fn = filename.split('.')[0]
        b = bytes(fn, 'utf-8')
        file_name_string = base64.urlsafe_b64encode(b)
        # set filename as random string
        filename = '{}.{}'.format(file_name_string, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("")




# Create your models here.
class Storm(models.Model):


    basins = [('AL','North Atlantic'),
              ('SL','South Atlantic'),
              ('EP','North East Pacific'),
              ('CP','North Central Pacific'),
              ('WP' ,'North West Pacific'),
              ('IO','North Indian OceanE'),
              ('SH','South Pacific Ocean')]

    image_keys=[
        ('ep','EP'),
        ('al','AT'),
    ]


    stormid = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=2)
    annual_cyclone_number=models.IntegerField(default=0)
    year = models.IntegerField(default=2017)


    def __str__(self):
        return self.stormid

    def return_id(self):
        return self.stormid

    def get_current_name(self):
        recent_adv = Advisory.objects.filter(stormid=self.id).order_by('-date')[0]
        return recent_adv.current_name

    def basin_name(self):
        b = [value for key, value in self.basins if key == self.region.upper()]
        return b[0]

    def peak_intensity(self):
        peak = Advisory.objects.filter(stormid=self.id).order_by('-category')[0]
        return peak.get_category_name()

    def last_observed(self):
        recent_adv = Advisory.objects.filter(stormid=self.id).order_by('-date')[0]
        return recent_adv.date

    def current_wind(self):
        current = Advisory.objects.filter(stormid=self.id).order_by('-date')[0]
        return current.max_sus_wind

    def image_url(self):
        prefix = self.stormid[:2]
        cc = self.stormid[2:4]
        url = [value for key, value in self.image_keys if key==prefix]
        print(url)
        return ("%s%s"%(url[0],cc))

    def max_wind_speed(self):
        adv = Advisory.objects.filter(stormid=self.id).order_by('-max_sus_wind')[0]
        return adv.max_sus_wind
class Advisory(models.Model):

    category_choices =[(1,'Subtropical Depression'),
                       (2,'Tropical Depression'),
                       (3,'Tropical Storm'),
                       (4, 'Tropical Cyclone'),
                       (5,'Hurricane'),
                       (0,'Remnants Of')]

    advisory_id = models.CharField(max_length=20)
    stormid = models.ForeignKey(Storm)
    date = models.DateTimeField()
    content = models.TextField()
    advisory_number = models.CharField(max_length=4)
    storm_location = models.CharField(max_length=10)
    max_sus_wind = models.IntegerField(default=None, null=True)
    category = models.IntegerField(choices=category_choices)
    current_name = models.CharField(default=None, null=True, max_length=40)

    def __str__(self):
        return "%s %s"%(self.current_name, self.advisory_id)

    def image_link(self):
        cyclone_num = self.stormid.return_id()
        region = cyclone_num[0].upper()
        return "%s%s"%(cyclone_num[2:4],region)

    def get_category_name(self):
        r = [value for key, value in self.category_choices if key == self.category ]
        return r[0]

class Posts(models.Model):
    image = models.ImageField(upload_to=path_and_rename,
                                      blank=True,
                                      null=True)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=75)

    def __str__(self):
        return self.title