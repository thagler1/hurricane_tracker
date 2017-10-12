from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.gis.db import models
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
    path = models.LineStringField(default=None, null=True)
    objects = models.GeoManager()


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
        return ("%s%s"%(url[0],cc))

    def latest_adv(self):
        current = Advisory.objects.filter(stormid=self.id).order_by('-date')[0]
        return current


    def max_wind_speed(self):
        adv = Advisory.objects.filter(stormid=self.id).order_by('-max_sus_wind')[0]
        return adv

    def max_wind_speed_api(self):
        adv = Advisory.objects.filter(stormid=self.id).order_by('-max_sus_wind')[0]
        return adv.max_sus_wind


    def all_advisories(self):
        return Advisory.objects.filter(stormid=self.id).order_by('date')

    def storm_data_api(self):
       advs = Advisory.objects.filter(stormid=self.id).order_by('date')
       keys = ['max_sus_wind']
       data_list = []
       for adv in advs:
           dict = adv.__dict__
           for k in keys:
              data_list.append({'date':adv.date.strftime("%Y-%m-%d-%H"), 'max_sus_wind':dict[k]})

       return data_list




    def first_seen(self):
        return Advisory.objects.filter(stormid=self.id).order_by('date')[0]

class Advisory(models.Model):

    saffir_simpson = [
        ((0,73),0),
        ((74,95),1),
        ((96,110),2),
        ((111,129),3),
        ((130,156),4),
        ((157,1000),5)
    ]

    category_choices =[(1,'Subtropical Depression'),
                       (2,'Tropical Depression'),
                       (3,'Tropical Storm'),
                       (4, 'Tropical Cyclone'),
                       (5,'Hurricane'),
                       (0,'Remnants Of')]

    advisory_id = models.CharField(max_length=75)
    stormid = models.ForeignKey(Storm)
    date = models.DateTimeField()
    content = models.TextField()
    advisory_number = models.CharField(max_length=4, default=None, null=True)
    storm_location = models.CharField(max_length=40)
    max_sus_wind = models.IntegerField(default=None, null=True)
    speed = models.IntegerField(default=None, null=True)
    min_cent_pressure = models.FloatField(default=None,null=True)
    coordinates = models.PointField(default=None, null=True)
    category = models.IntegerField(choices=category_choices)
    current_name = models.CharField(default=None, null=True, max_length=40)
    lat = models.FloatField(default=None, null=True)
    long = models.FloatField(default=None, null=True)
    
    

    def __str__(self):
        return "%s %s"%(self.current_name, self.advisory_id)

    def image_link(self):
        cyclone_num = self.stormid.return_id()
        region = cyclone_num[0].upper()
        return "%s%s"%(cyclone_num[2:4],region)

    def get_category_name(self):
        r = [value for key, value in self.category_choices if key == self.category ]
        return r[0]

    def saffir_scale(self):
        scale = self.saffir_simpson
        current_winds = self.max_sus_wind

        for r, cat in scale:
            low = r[0]
            high = r[1]
            if current_winds >= low and current_winds <= high:
                return cat



class Posts(models.Model):
    image = models.ImageField(upload_to=path_and_rename,
                                      blank=True,
                                      null=True)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=75)
    target = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class cities(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    coords = models.PointField(default=None, null=True)
    population = models.FloatField()
    objects = models.GeoManager()

    def __str__(self):
        return self.name + " " + self.state
