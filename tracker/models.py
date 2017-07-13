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
class Advisory(models.Model):
    advisory_id = models.CharField(max_length=20)
    stormid = models.ForeignKey(Storm)
    date = models.DateTimeField()
    content = models.TextField()
    advisory_number = models.CharField(max_length=4)
    storm_location = models.CharField(max_length=10)
    max_sus_wind = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s %s"%(self.stormid, self.date, self.advisory_id)

