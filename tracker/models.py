from django.db import models

# Create your models here.
class Storm(models.Model):
    stormid = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=2)
    annual_cyclone_number=models.IntegerField(default=0)
    year = models.IntegerField(default=2017)


    def __str__(self):
        return self.stormid

    def return_id(self):
        return self.stormid
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
    max_sus_wind = models.CharField(max_length=10)
    category = models.IntegerField(choices=category_choices)

    def __str__(self):
        return "%s %s %s"%(self.stormid, self.date, self.advisory_id)

    def image_link(self):
        cyclone_num = self.stormid.return_id()
        region = cyclone_num[0].upper()
        return "%s%s"%(cyclone_num[2:4],region)

