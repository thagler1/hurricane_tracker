from ..models import *
from rest_framework import serializers






class StormSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Storm
        fields = ('get_current_name', 'stormid', 'peak_intensity', 'max_wind_speed_api', 'storm_data_api')


class SeasonSerializer(serializers.Serializer):
    stormid = serializers.CharField(max_length =15)
    storm_location = serializers.CharField(max_length=40)
    max_sus_wind = serializers.IntegerField()
    speed = serializers.IntegerField()
    min_cent_pressure = serializers.FloatField()

class DeltaSpeedSerializer(serializers.Serializer):
    delta_speed = serializers.IntegerField()
    delta_wind = serializers.IntegerField()